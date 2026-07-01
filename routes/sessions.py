from flask import Blueprint, jsonify, request  # Blueprint: groups related routes, jsonify: converts python data to JSON HTTP responses,request: gives access to incoming HTTP request data.
from extensions import db                      # db: SQLAlchemy database instance. 
from models import Session                     # model representing an individual teaching session belonging to a class group.

# These imports connect Flask's routing tooks, the database layer, and the Session model.
# Together, they allow this file to act as the dedicated API surface for session operations. 

sessions_bp = Blueprint('sessions', __name__)   # Creates a blueprint named "sessions"

# GET all sessions for a class group.
@sessions_bp.route("/classgroups/<int:group_id>/sessions", methods=["GET"]) # defines an endpoint that retrieves all sessions to a specific class group.
def get_sessions(group_id):
    sessions = Session.query.filter_by(classgroup_id=group_id).all() # queries the database for all session objects whose classgroup_id matches the given group.
    return jsonify([s.to_dict() for s in sessions])                 # converts each session model instance into a JSON-safe dictionary.

# POST create a sessoin for a class group. 
@sessions_bp.route("/classgroups/<int:group_id>/sessions", methods=["POST"]) # endpoint for creating a new session under a specif class group .
def create_session(group_id):
    data = request.json                                              # reads the JSON payload sent by the client. 
    session = Session(
        classgroup_id=group_id,   # taken from the URL
        date=data["date"],        
        topic=data.get("topic")
    )
    db.session.add(session)                                          # adds the new session to the database session. 
    db.session.commit()                                              # saves it permanently.
    return jsonify(session.to_dict()), 201                           # returns the newly created session with HTTP status 201 created. 

# GET a single session. 
@sessions_bp.route("/sessions/<int:id>", methods=["GET"]) # endpoint to fethc a single session by its ID.
def get_session(id):
    session = Session.query.get_or_404(id)        # attemps to retrieve the session, if not found, automatically return a 404 error.
    return jsonify(session.to_dict())             # returns the session as JSON.