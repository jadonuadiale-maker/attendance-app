import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from utils.session_auto import auto_create_sessions
from datetime import date, datetime
from extensions import db
from models import *
from routes.classgroups import classgroups_bp
from routes.sessions import sessions_bp
from routes.users import users_bp, assign_classgroup_from_dob 
from routes.auth import auth_bp
from routes.reports import reports_bp
from utils.auth_utils import login_required, role_required

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

scheduler = BackgroundScheduler()

def run_auto_create():
    with app.app_context():
        auto_create_sessions()

scheduler.add_job(run_auto_create, 'interval', minutes=1)

# BLUEPRINT REGISTRATION.
# Class groups and session routes are modlurized into
# separate blueprints foir cleaner structure.
app.register_blueprint(classgroups_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)

# FIRST PAGE -> LOGIN.
@app.route('/')
def index():
    return redirect(url_for('auth.login_page'))

# DASHBOARD PAGE (updated)
@app.route('/dashboard')
@login_required
@role_required("admin", "teacher")
def dashboard():
    today = date.today().isoformat()

    # --- Role-aware session filtering ---
    role = session.get("role")
    user_id = session.get("user_id")

    if role == "teacher":
        teacher = User.query.get(user_id)
        sessions = Session.query.filter_by(
            classgroup_id=teacher.classgroup_id,
            date=today
        ).all()
    else:
        sessions = Session.query.filter_by(date=today).all()

    # --- Build per-session attendance summary ---
    summary = {}

    for s in sessions:
        records = AttendanceRecord.query.filter_by(session_id=s.id).all()

        service1 = sum(1 for r in records if r.service_number == 1)
        service2 = sum(1 for r in records if r.service_number == 2)
        both = sum(1 for r in records if r.service_number == 3)
        total = len(records)

        summary[s.id] = {
            "group_name": s.classgroup.name,
            "service1": service1,
            "service2": service2,
            "both": both,
            "total": total,
            "session": s
        }

    return render_template("dashboard.html", summary=summary)


# USER PAGE - List All Users.
@app.route('/users')
@login_required
@role_required("admin", "teacher")
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# ADD USER - Form Submission.
@app.route('/add_user', methods=['POST'])
def add_user():
    first = request.form['first_name']
    surname = request.form['surname']
    dob_raw = request.form.get('date_of_birth')
    dob = datetime.strptime(dob_raw, "%Y-%m-%d").date() if dob_raw else None

    group = assign_classgroup_from_dob(dob)

    user = User(
        first_name=first,
        surname=surname,
        full_name=f"{first} {surname}",
        date_of_birth=dob,
        date_joined=date.today(),
        classgroup_id=group.id if group else None
    )

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users'))


# DELETE USER - Utility Route (admin only).
@app.route('/delete_user/<int:id>', methods=['POST'])
@login_required
@role_required("admin")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

# ATTENDANCE RECORDS PAGE.
@app.route('/attendance')
@login_required
@role_required("admin", "teacher")
def attendance():
    records = AttendanceRecord.query.all()
    sessions = Session.query.all()
    return render_template('attendance.html', records=records, sessions=sessions)

# AUTOCOMPLETE USERS SEARCH.
@app.route("/users/search")
def search_users():
    q = request.args.get("q", "")
    users = User.query.filter(User.full_name.ilike(f"%{q}%")).all()
    return jsonify([u.to_dict() for u in users])

# APP RUNNER.
if __name__ == '__main__':
    scheduler.start()
    app.run(debug=False)