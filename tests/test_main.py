from fastapi.testclient import TestClient
from main import app, populate_dummy_data, SessionLocal

client = TestClient(app)

def setup_module(module):
    db = SessionLocal()
    populate_dummy_data()
    db.close()

def test_overall_leaderboard():
    response = client.get("/overall_leaderboard/")
    assert response.status_code == 200
    leaderboard = response.json()
    assert isinstance(leaderboard, list)
    assert len(leaderboard) > 0

def test_twos_leaderboard():
    response = client.get("/twos_leaderboard/")
    assert response.status_code == 200
    leaderboard = response.json()
    assert isinstance(leaderboard, list)
    assert len(leaderboard) > 0
