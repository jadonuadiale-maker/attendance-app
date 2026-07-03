from flask import Blueprint, jsonify, request, render_template, url_for, redirect # Blueprint: groups related routes, jsonify: converts python data to JSON HTTP responses,request: gives access to incoming HTTP request data, render template: for html page view. 
from extensions import db                      # db: SQLAlchemy database instance. 
from models import Session                     # model representing an individual teaching session belonging to a class group.

# These imports connect Flask's routing tooks, the database layer, and the Session model.
# Together, they allow this file to act as the dedicated API surface for session operations. 

sessions_bp = Blueprint('sessions', __name__)   # Creates a blueprint named "sessions"

# Simple session overview route.
@sessions_bp.route("/sessions", methods=["GET"])
def sessions_overview():
    sessions = Session.query.all()
    return jsonify([s.to_dict() for s in sessions])

# Session overview route for HTML page. 
@sessions_bp.route('/sessions/view', methods=['GET'])
def sessions():
    from models import ClassGroup
    groups = ClassGroup.query.all()
    sessions = Session.query.all()
    return render_template('sessions.html', sessions=sessions, groups=groups)

# GET all sessions for a class group.
@sessions_bp.route("/classgroups/<int:group_id>/sessions", methods=["GET"]) # defines an endpoint that retrieves all sessions to a specific class group.
def get_sessions(group_id):
    sessions = Session.query.filter_by(classgroup_id=group_id).all() # queries the database for all session objects whose classgroup_id matches the given group.
    return jsonify([s.to_dict() for s in sessions])                 # converts each session model instance into a JSON-safe dictionary.

# POST create a session for a class group. 

# For HTML view.
@sessions_bp.route('/sessions/create', methods=['POST'])
def create_session_html():
    data = request.form
    group_id = data.get('group_id')
    session = Session(
        classgroup_id=group_id,
        date=data['date'],
        topic=data.get('topic')
    )
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('sessions.sessions'))

# For API testing.
@sessions_bp.route("/classgroups/<int:group_id>/sessions", methods=["POST"]) # endpoint for creating a new session under a specif class group .
def create_session_api(group_id):
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

# For HTML view. 
@sessions_bp.route("/sessions/<int:id>/view", methods=["GET"])
def view_session(id):
    session = Session.query.get_or_404(id)
    return render_template("session_detail.html", session=session)


# For API testing
@sessions_bp.route("/sessions/<int:id>", methods=["GET"]) # endpoint to fethc a single session by its ID.
def get_session(id):
    session = Session.query.get_or_404(id)        # attemps to retrieve the session, if not found, automatically return a 404 error.
    return jsonify(session.to_dict())             # returns the session as JSON.