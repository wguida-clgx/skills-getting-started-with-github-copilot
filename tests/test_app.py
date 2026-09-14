from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    # ensure participant is not present before the test
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert unregister_response.status_code == 200
    assert email not in unregister_response.json()["participants"]
