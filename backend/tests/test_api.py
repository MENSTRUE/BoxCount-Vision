import io
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health_contract():
    r=client.get('/api/v1/health')
    assert r.status_code==200 and 'model_present' in r.json()

def test_experiments_readonly():
    r=client.get('/api/v1/experiments')
    assert r.status_code==200 and 'detection' in r.json()

def test_history():
    r=client.get('/api/v1/history')
    assert r.status_code==200 and isinstance(r.json()['items'],list)

def test_reject_invalid_extension():
    r=client.post('/api/v1/analyze/image',files={'file':('malicious.exe',b'x','application/octet-stream')})
    assert r.status_code==415

def test_invalid_image():
    r=client.post('/api/v1/analyze/image',files={'file':('bad.png',b'invalid','image/png')})
    assert r.status_code==422

def test_prevent_file_traversal():
    assert client.get('/api/v1/files/not-a-uuid.jpg').status_code==404
