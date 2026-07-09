from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date, datetime
from extensions import db
from models import User, AttendanceRecord, Session

users_bp = Blueprint("users", __name__)

@users_bp.route("/first_timer/<int:session_id>")
def first_timer(session_id):
    return render_template("first_timer.html", session_id=session_id)


@users_bp.route("/first_timer/submit", methods=["POST"])
def submit_first_timer():
    first_name = request.form.get("first_name")
    surname = request.form.get("surname")
    from datetime import datetime
    dob_raw = request.form.get("date_of_birth")
    dob = datetime.strptime(dob_raw, "%Y-%m-%d").date() if dob_raw else None
    session_id = request.form.get("session_id")
    service_number = int(request.form.get("service_number"))

    user = User(
        first_name=first_name,
        surname=surname,
        full_name=f"{first_name} {surname}",
        date_of_birth=dob,
        date_joined=date.today()
    )

    db.session.add(user)
    db.session.commit()

    record = AttendanceRecord(
        user_id=user.id,
        session_id=session_id,
        date=date.today(),
        status="present",
        service_number=service_number
    )

    db.session.add(record)
    db.session.commit()

    return redirect(url_for("sessions.checkin_view", id=session_id))
