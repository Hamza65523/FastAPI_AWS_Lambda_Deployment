from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/pre_process_query?text= Best burger best pizza")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}