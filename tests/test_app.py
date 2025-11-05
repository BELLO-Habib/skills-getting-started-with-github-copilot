from fastapi.testclient import TestClient
import pytest
from urllib.parse import quote

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic shape checks
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "pytest.user+unregister@example.com"

    # Ensure clean start
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up (URL-encode query param so '+' isn't interpreted as space)
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(test_email)}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{quote(activity)}/signup?email={quote(test_email)}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(test_email)}")
    assert resp_un.status_code == 200
    assert test_email not in activities[activity]["participants"]

    # Unregister again should fail
    resp_un2 = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(test_email)}")
    assert resp_un2.status_code == 400
