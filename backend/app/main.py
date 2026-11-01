"""BoxCount Vision — honest research inference API.
Models are loaded from a trusted local file only, never from uploaded paths.
"""
from __future__ import annotations
import csv
import io
import json
import logging
import os
import tempfile
import threading
import time
from collections import Counter
from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / 'backend'

# Support .env without requiring changes to the system environment.
try:
    from dotenv import load_dotenv
    load_dotenv(BACKEND / '.env', override=False)
except ImportError:
    pass

MODEL_REL = os.getenv('BOXCOUNT_MODEL_PATH', '../models/champion/boxcount_champion.pt')
MODEL_PATH = Path(MODEL_REL)
if not MODEL_PATH.is_absolute():
    MODEL_PATH = (BACKEND / MODEL_PATH).resolve()
MAX_UPLOAD = max(1, int(os.getenv('BOXCOUNT_MAX_UPLOAD_MB','100'))) * 1024**2
MAX_SECONDS = max(1, int(os.getenv('BOXCOUNT_MAX_VIDEO_SECONDS','120')))
SAMPLE_FPS = max(.2, float(os.getenv('BOXCOUNT_VIDEO_SAMPLE_FPS','3')))
MAX_FRAMES = max(1, int(os.getenv('BOXCOUNT_MAX_VIDEO_FRAMES','360')))
CONF = float(os.getenv('BOXCOUNT_CONFIDENCE','0.25'))
IOU = float(os.getenv('BOXCOUNT_IOU','0.5'))
IMGSZ = int(os.getenv('BOXCOUNT_IMAGE_SIZE','640'))
DEVICE = os.getenv('BOXCOUNT_DEVICE','cpu')
ORIGINS = [s.strip() for s in os.getenv('BOXCOUNT_CORS_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(',') if s.strip()]
OUTPUTS = BACKEND / 'outputs'
OUTPUTS.mkdir(parents=True,exist_ok=True)

app = FastAPI(title='BoxCount Vision API', version='1.0.0', description='Research-only cardboard detection and counting, using an authentic local YOLO artifact.')
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_credentials=False, allow_methods=['GET','POST'], allow_headers=['*'])
_model = None
_model_lock = threading.Lock()
_inference_lock = threading.Lock()
_history: list[dict] = []

class ImageAnalysis(BaseModel):
    id: str
    kind: str
    filename: str
    count: int
    confidence: float
    processed_at: float
    width: int
    height: int
    detections: list[dict]
    preview_url: str
    elapsed_ms: float
    research_only: bool = True


def resolve_model():
    # Convenient compatibility with the screenshot where the model is under baseline.
    candidate = ROOT / 'models' / 'baseline' / 'boxcount_champion.pt'
    return MODEL_PATH if MODEL_PATH.exists() else (candidate if candidate.exists() else MODEL_PATH)


def load_model():
    global _model
    if _model is None:
        path = resolve_model()
        if not path.is_file():
            raise HTTPException(503, detail=f'Model not found; move trusted Kaggle boxcount_champion.pt to models/champion/ (or set BOXCOUNT_MODEL_PATH). Looked for: {path}')
        with _model_lock:
            if _model is None:
                try:
                    from ultralytics import YOLO
                    _model = YOLO(str(path))
                except Exception as e:
                    logger.exception('Model load failure')
                    raise HTTPException(503, detail=f'Model failed to load: {type(e).__name__}. Check Ultralytics/PyTorch compatibility in backend logs.') from e
    return _model


def parse_result(result, width: int, height: int):
    detections=[]
    boxes = getattr(result,'boxes',None)
    if boxes is not None:
        for b in boxes:
            try:
                xyxy=b.xyxy[0].detach().cpu().tolist()
                score=float(b.conf[0].item())
                cls=int(b.cls[0].item())
                if cls != 0:  # single-class research contract
                    continue
                x1,y1,x2,y2 = [float(v) for v in xyxy]
                detections.append({'box':[round(max(0,min(width,v)),2) if i%2==0 else round(max(0,min(height,v)),2) for i,v in enumerate([x1,y1,x2,y2])], 'confidence':round(score,5), 'class_id':cls})
            except Exception as e:
                logger.warning('Skipping malformed detection: %s',e)
    return detections


def infer_frame(frame):
    h,w=frame.shape[:2]
    with _inference_lock:
        try:
            result=load_model().predict(source=frame,conf=CONF,iou=IOU,imgsz=IMGSZ,device=DEVICE,verbose=False)[0]
        except HTTPException:
            raise
        except Exception as e:
            logger.exception('Inference failure')
            raise HTTPException(500, detail=f'Inference failed: {type(e).__name__}. See backend logs.') from e
    return parse_result(result,w,h)


def draw(frame,detections):
    result=frame.copy()
    for item in detections:
        x1,y1,x2,y2=map(int,item['box'])
        cv2.rectangle(result,(x1,y1),(x2,y2),(60,178,116),2)
        cv2.putText(result,f"BOX {item['confidence']:.2f}",(x1,max(20,y1-8)),cv2.FONT_HERSHEY_SIMPLEX,.55,(60,178,116),2,cv2.LINE_AA)
    return result


async def read_upload(file: UploadFile, allowed: set[str]):
    name = Path(file.filename or 'upload').name
    extension=Path(name).suffix.lower()
    if extension not in allowed:
        raise HTTPException(415,detail=f'Unsupported file type {extension or "(none)"}. Allowed: {sorted(allowed)}')
    blob=await file.read(MAX_UPLOAD+1)
    if len(blob)>MAX_UPLOAD:
        raise HTTPException(413,detail='File exceeds upload size limit')
    if not blob:
        raise HTTPException(400,detail='Empty file')
    return name,extension,blob


def save_jpeg(frame,uid):
    ok,encoded=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,85])
    if not ok: raise HTTPException(500,detail='Could not generate preview')
    path=OUTPUTS / f'{uid}.jpg'
    path.write_bytes(encoded.tobytes())
    return f'/api/v1/files/{uid}.jpg'


@app.get('/api/v1/health')
def health():
    path=resolve_model()
    return {'status':'ok','model_present':path.is_file(),'model_loaded':_model is not None,'model_filename':path.name,'research_only':True,'api_version':'1.0.0'}

@app.get('/api/v1/experiments')
def experiments():
    def csvrows(rel):
        p=ROOT/rel
        if not p.is_file():return []
        with p.open(newline='',encoding='utf-8-sig') as f:
            return list(csv.DictReader(f))[:150]
    report_path=ROOT/'reports/experiments/research_report.json'
    try:
        report=json.loads(report_path.read_text(encoding='utf-8')) if report_path.is_file() else None
    except (ValueError, OSError): report=None
    return {'research_report':report,'detection':csvrows('reports/evaluation/final_heldout_detection_metrics.csv'),'counting':csvrows('reports/evaluation/heldout_count_metrics.csv'),'selection':csvrows('reports/experiments/validation_model_selection.csv'),'source':'saved_local_kaggle_artifacts','research_only':True}

@app.get('/api/v1/history')
def history():
    return {'items':list(reversed(_history[-30:]))}

@app.get('/api/v1/files/{filename}')
def file_view(filename: str):
    if not filename.endswith('.jpg') or len(filename)!=36 or not all(c in '0123456789abcdef' for c in filename[:-4]):
        raise HTTPException(404,detail='Not found')
    f=OUTPUTS/filename
    if not f.is_file(): raise HTTPException(404,detail='Not found')
    return FileResponse(f,media_type='image/jpeg',headers={'Cache-Control':'private, max-age=3600'})

@app.post('/api/v1/analyze/image',response_model=ImageAnalysis)
async def analyze_image(file:UploadFile=File(...)):
    name,ext,data=await read_upload(file,{'.jpg','.jpeg','.png','.webp','.bmp'})
    frame=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
    if frame is None: raise HTTPException(422,detail='Invalid image bytes')
    if frame.shape[0]*frame.shape[1]>30_000_000: raise HTTPException(413,detail='Image exceeds 30 megapixels')
    t=time.perf_counter()
    ds=infer_frame(frame)
    uid=uuid4().hex
    preview=save_jpeg(draw(frame,ds),uid)
    result=ImageAnalysis(id=uid,kind='image',filename=name,count=len(ds),confidence=CONF,processed_at=time.time(),width=frame.shape[1],height=frame.shape[0],detections=ds,preview_url=preview,elapsed_ms=round((time.perf_counter()-t)*1000,1))
    _history.append(result.model_dump(exclude={'detections'}))
    return result

@app.post('/api/v1/analyze/video')
async def analyze_video(file:UploadFile=File(...)):
    name,ext,data=await read_upload(file,{'.mp4','.avi','.mov','.mkv','.webm'})
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as f:
            tmp=f.name;f.write(data)
        cap=cv2.VideoCapture(tmp)
        if not cap.isOpened(): raise HTTPException(422,detail='Unreadable video or unsupported codec')
        try:
            fps=float(cap.get(cv2.CAP_PROP_FPS))
            frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if not np.isfinite(fps) or fps<=0: raise HTTPException(422,detail='Invalid video FPS')
            if frame_count<=0: raise HTTPException(422,detail='Cannot determine video frame count')
            duration=frame_count/fps
            if duration>MAX_SECONDS: raise HTTPException(413,detail=f'Video duration exceeds {MAX_SECONDS}s limit')
            stride=max(1,round(fps/SAMPLE_FPS))
            timeline=[];first_preview=None;processed=0
            t=time.perf_counter()
            # Sparse frame sampling; not object tracking. No counts are added across frames.
            index=0
            while processed<MAX_FRAMES:
                success,frame=cap.read()
                if not success:break
                if index%stride==0:
                    ds=infer_frame(frame)
                    count=len(ds)
                    timeline.append({'time_s':round(index/fps,3),'count':count})
                    if first_preview is None:first_preview=draw(frame,ds)
                    processed+=1
                index+=1
            if not timeline:raise HTTPException(422,detail='No frames decoded')
            uid=uuid4().hex
            preview=save_jpeg(first_preview,uid)
            item={'id':uid,'kind':'video','filename':name,'processed_at':time.time(),'sampled_frames':len(timeline),'duration_s':round(duration,2),'fps':fps,'confidence':CONF,'timeline':timeline,'average_count':round(float(np.mean([x['count'] for x in timeline])),3),'peak_count':max(x['count'] for x in timeline),'preview_url':preview,'elapsed_ms':round((time.perf_counter()-t)*1000,1),'research_only':True,'tracking_enabled':False,'count_definition':'per-frame detections (no cross-frame identity)'}
            _history.append({k:v for k,v in item.items() if k!='timeline'})
            return item
        finally:cap.release()
    finally:
        if tmp:
            try:os.remove(tmp)
            except OSError:logger.warning('Could not remove temporary video %s',tmp)
