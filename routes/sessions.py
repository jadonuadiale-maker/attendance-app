from flask import Blueprint, jsonify, request, render_template, url_for, redirect, session as flask_session # Blueprint: groups related routes, jsonify: converts python data to JSON HTTP responses,request: gives access to incoming HTTP request data, render template: for html page view. 
from extensions import db                      # db: SQLAlchemy database instance. 
from models import AttendanceRecord, User, Session, ClassGroup                     # model representing an individual teaching session belonging to a class group.
from datetime import date
from utils.auth_utils import login_required, role_required

# These imports connect Flask's routing tooks, the database layer, and the Session model.
# Together, they allow this file to act as the dedicated API surface for session operations. 

# --- AUTO-CREATE SESSIONS FOR TODAY ---
def auto_create_sessions():
    today = date.today().isoformat()
    created_sessions = []
    # Fetch all class groups (2-6, 7-12, Teens)
    groups = ClassGroup.query.all()

    for group in groups:
        # Prevent duplicates
        existing = Session.query.filter_by(
            classgroup_id=group.id,
            date=today
        ).first()

        if existing:
            continue

        # Create session for this group
        session = Session(
            classgroup_id=group.id,
            date=today,
            topic="Sunday Service"
        )

        db.session.add(session)
        created_sessions.append(session)

    db.session.commit()
    return created_sessions


sessions_bp = Blueprint('sessions', __name__)   # Creates a blueprint named "sessions"

# Simple session overview route.
@sessions_bp.route("/sessions", methods=["GET"])
def sessions_overview():
    sessions = Session.query.all()
    return jsonify([s.to_dict() for s in sessions])

# Session overview route for HTML page. 
@sessions_bp.route('/sessions/view', methods=['GET'])
@login_required
@role_required("admin", "teacher")
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

# POST CREATE A SESSION FOR A CLASS GROUP. 

# For HTML view (admin only).
@sessions_bp.route('/sessions/create', methods=['POST'])
@login_required
@role_required("admin")
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

# For API testing (admin only).
@sessions_bp.route("/classgroups/<int:group_id>/sessions", methods=["POST"]) # endpoint for creating a new session under a specif class group .
@login_required
@role_required("admin")
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

# For Auto-Creation (admin only).
@sessions_bp.route("/sessions/auto_create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def auto_create():
    created = auto_create_sessions()   # Only daily logic is needed. 
    return redirect(url_for('sessions.sessions'))

# GET a single session. 

# For HTML view. 
@sessions_bp.route("/sessions/<int:id>/view", methods=["GET"])
@login_required
@role_required("admin", "teacher")
def view_session(id):
    session = Session.query.get_or_404(id)

    # --- Teacher scoping ---
    if flask_session.get("role") == "teacher":
        teacher = User.query.get(flask_session.get("user_id"))
        if teacher.classgroup_id != session.classgroup_id:
            return "Unauthorized", 403

    return render_template("session_detail.html", session=session)


# For API testing
@sessions_bp.route("/sessions/<int:id>", methods=["GET"]) # endpoint to fethc a single session by its ID.
def get_session(id):
    session = Session.query.get_or_404(id)        # attemps to retrieve the session, if not found, automatically return a 404 error.
    return jsonify(session.to_dict())             # returns the session as JSON.

# Check-in page (per session, per pad)
@sessions_bp.route("/sessions/<int:id>/checkin/view", methods=["GET"])
def checkin_view(id):
    session = Session.query.get_or_404(id)

    # --- Ensure session is for today (avoids stale pads) ---
    today = date.today().isoformat()
    if session.date != today:
        return render_template(
            "error.html",
            message="This session is not for today. Please refresh or use the correct pad."
        )

    # --- Filter users by class group of this session(pad-specific view) ---
    users = User.query.filter_by(classgroup_id=session.classgroup_id) \
                      .order_by(User.full_name.asc()).all()
    return render_template("checkin.html", session_id=id, session=session, users=users)


# Check-in detail page (2-step flow)
@sessions_bp.route("/checkin/<int:user_id>/<int:session_id>")
def checkin_detail(user_id, session_id):
    user = User.query.get_or_404(user_id)
    session = Session.query.get_or_404(session_id)

    # --- Block cross-group check-ins ---
    if user.classgroup_id != session.classgroup_id:
        return render_template(
            "error.html",
            message="This user does not belong to this class group."
        )

    # --- Ensure session is for today ---
    today = date.today().isoformat()
    if session.date != today:
        return render_template(
            "error.html",
            message="This session is not for today. Please refresh or use the correct pad."
        )

    # --- If already checked in, show info instead of form ---
    existing = AttendanceRecord.query.filter_by(
        user_id=user.id,
        session_id=session.id
    ).first()

    if existing:
        return render_template(
            "already_checked_in.html",
            user=user,
            session=session,
            record=existing
        )

    return render_template("checkin_detail.html", user=user, session=session)


# API check-in (used by UI submit)
@sessions_bp.route("/sessions/<int:session_id>/checkin", methods=["POST"])
def checkin(session_id):
    data = request.json
    user_id = data.get("user_id")
    service_number = data.get("service_number")  # 1, 2, or 3 ("both")

    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if service_number not in [1, 2, 3]:
        return jsonify({"error": "Invalid service number"}), 400

    # --- One record per user per session: update instead of duplicate ---
    existing = AttendanceRecord.query.filter_by(
    user_id=user_id,
    session_id=session_id
).first()

    # --- Reject duplicate check-ins (tests expect 400) ---
    if existing:
        return jsonify({"error": "User already checked in"}), 400


    record = AttendanceRecord(
        user_id=user_id,
        session_id=session_id,
        date=session.date, # ensures consistency with session date. 
        status="present",
        service_number=service_number
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Check-in successful"}), 201


# UI submit check-in (form-based)
@sessions_bp.route("/checkin/submit", methods=["POST"])
def submit_checkin():
    user_id = int(request.form.get("user_id"))
    session_id = int(request.form.get("session_id"))
    service_number = int(request.form.get("service_number"))

    existing = AttendanceRecord.query.filter_by(
        user_id=user_id,
        session_id=session_id
    ).first()

    if existing:
        existing.service_number = service_number
        existing.status = "present"
        db.session.commit()
        return redirect(url_for("sessions.checkin_view", id=session_id))

    session = Session.query.get(session_id)

    record = AttendanceRecord(
        user_id=user_id,
        session_id=session_id,
        date=session.date,  # ensures consistency with date
        status="present",
        service_number=service_number
    )

    db.session.add(record)
    db.session.commit()

    return redirect(url_for("sessions.checkin_view", id=session_id))


# Admin override route (admin only).
@sessions_bp.route("/attendance/<int:record_id>/override", methods=["POST"])
@login_required
@role_required("admin")
def override_attendance(record_id):
    record = AttendanceRecord.query.get_or_404(record_id)

    new_status = request.form.get("status")
    new_service = request.form.get("service_number")

    # --- Admin can fix status/service safely ---
    if new_status:
        record.status = new_status
    if new_service:
        record.service_number = int(new_service)

    db.session.commit()
    return redirect(url_for("sessions.attendance_view", id=record.session_id))

# Attendance Marking UI.
@sessions_bp.route("/sessions/<int:id>/attendance/view")
@login_required
@role_required("admin", "teacher")
def attendance_view(id):
    session = Session.query.get_or_404(id)

    # --- Teacher scoping ---
    if flask_session.get("role") == "teacher":
        teacher = User.query.get(flask_session.get("user_id"))
        if teacher.classgroup_id != session.classgroup_id:
            return "Unauthorized", 403

    records = AttendanceRecord.query.filter_by(session_id=id).all()
    return render_template("attendance_marking.html", session=session, records=records)
