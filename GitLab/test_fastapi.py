import pytest
from fastapi.testclient import TestClient
from myapi import app

client = TestClient(app)

def test_predict_sales():
    payload = {
        "shop_id": 1,
        "item_id": 101,
        "item_price": 100.0,
        "date_block_num": 1
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_retrain_model():
    response = client.post("/train")
    assert response.status_code == 200
    assert response.json()["message"] == "Modèle réentraîné et sauvegardé avec succès."
