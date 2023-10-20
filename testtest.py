from fastapi import FastAPI
from fastapi.testclient import TestClient

from test import app

client=TestClient(app)

def test_read_root():
    response=client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello":"World"}