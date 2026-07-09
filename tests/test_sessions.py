from models import User, Session, AttendanceRecord
from extensions import db

# Internal commentary:
# - Tests search endpoint.
# - Tests check-in creation.
# - Tests duplicate prevention.

def test_user_search(client):
    res = client.get("/users/search?q=a")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_checkin_success(client):
    # Create user + session.
    user = User(name="TestUser")
    session = Session(classgroup_id=1, date="2026-07-07")
    db.session.add_all([user, session])
    db.session.commit()

    res = client.post(f"/sessions/{session.id}/checkin", 
                      json={"user_id": user.id, "service_number": 1}
    )
    assert res.status_code == 201

def test_duplicate_checkin(client):
    user = User(name="TestUser2")
    session = Session(classgroup_id=1, date="2026-07-07")
    db.session.add_all([user, session])
    db.session.commit()

    # First check-in.
    client.post(f"/sessions/{session.id}/checkin", 
                json={"user_id": user.id, "service_number": 1}
    )

    # Duplicate for same service.
    res = client.post(f"/sessions/{session.id}/checkin", 
                      json={"user_id": user.id, "service_number": 1}
    )
    assert res.status_code == 400