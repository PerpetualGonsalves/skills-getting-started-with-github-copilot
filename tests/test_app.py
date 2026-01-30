import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    # Use a unique email to avoid collision
    email = "testuser1@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Chess Club" in response.json().get("message", "")

    # Clean up: remove the test user
    data = client.get("/activities").json()
    data["Chess Club"]["participants"].remove(email)

def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"  # Already in Chess Club
    response = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_signup_for_activity_not_found():
    email = "testuser2@mergington.edu"
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
