from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import date, datetime
from extensions import db
from models import User, AttendanceRecord, Session, ClassGroup

users_bp = Blueprint("users", __name__)


def assign_classgroup_from_dob(dob):
    # --- Simple age-based mapping (placeholder logic) ---
    if not dob:
        return ClassGroup.query.filter_by(name="Teens").first()  # default

    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if 2 <= age <= 6:
        return ClassGroup.query.filter_by(name="2-6").first()
    elif 7 <= age <= 12:
        return ClassGroup.query.filter_by(name="7-12").first()
    elif age >= 13:
        return ClassGroup.query.filter_by(name="Teens").first()


@users_bp.route("/first_timer/<int:session_id>")
def first_timer(session_id):
    # --- Pad-specific first timer entry page ---
    return render_template("first_timer.html", session_id=session_id)


@users_bp.route("/first_timer/submit", methods=["POST"])
def submit_first_timer():
    first_name = request.form.get("first_name")
    surname = request.form.get("surname")
    dob_raw = request.form.get("date_of_birth")
    session_id_from_pad = int(request.form.get("session_id"))
    service_number = int(request.form.get("service_number"))

    dob = datetime.strptime(dob_raw, "%Y-%m-%d").date() if dob_raw else None

    # --- Check if user already exists ---
    existing_user = User.query.filter_by(full_name=f"{first_name} {surname}").first()
    if existing_user:
        user = existing_user
    else:
        user = User(
            first_name=first_name,
            surname=surname,
            full_name=f"{first_name} {surname}",
            date_of_birth=dob,
            date_joined=date.today()
        )

        # --- Add and commit user ---
        db.session.add(user)
        db.session.commit()

    # --- Assign correct class group based on DOB ---
    assigned_group = assign_classgroup_from_dob(dob)
    user.classgroup_id = assigned_group.id
    db.session.commit()
    
    # --- Fetch today's session for assigned class group ---
    today = date.today().isoformat()

    correct_session = Session.query.filter_by(
        classgroup_id=assigned_group.id,
        date=today
    ).first()

    # --- Store attendance in correct class group session ---
    record = AttendanceRecord(
        user_id=user.id,
        session_id=correct_session.id,
        date=date.today(),
        status="present",
        service_number=service_number
    )

    db.session.add(record)
    db.session.commit()

    # --- Tell them which pad to use next time ---
    return render_template(
        "first_timer_success.html",
        user=user,
        assigned_group=assigned_group,
        pad_session_id=session_id_from_pad
    )

# Class group aware autcomplete search point. 
@users_bp.route("/users/search_by_group")
def search_by_group():
    q = request.args.get("q", "")
    group_id = request.args.get("group_id", type=int)

    users = User.query.filter(
        User.classgroup_id == group_id,
        User.full_name.ilike(f"%{q}%")
    ).order_by(User.full_name.asc()).all()

    return jsonify([u.to_dict() for u in users])



# Admin add user (no attendance)
@users_bp.route("/admin/users/create")
def admin_create_user():
    return render_template("admin_add_user.html")


@users_bp.route("/admin/users/submit", methods=["POST"])
def admin_submit_user():
    first_name = request.form.get("first_name")
    surname = request.form.get("surname")
    dob_raw = request.form.get("date_of_birth")

    dob = datetime.strptime(dob_raw, "%Y-%m-%d").date() if dob_raw else None

    user = User(
        first_name=first_name,
        surname=surname,
        full_name=f"{first_name} {surname}",
        date_of_birth=dob,
        date_joined=date.today()
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("users"))
