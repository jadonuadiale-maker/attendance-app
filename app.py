from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_migrate import Migrate
from datetime import date, datetime
from extensions import db
from models import *
from routes.classgroups import classgroups_bp
from routes.sessions import sessions_bp
from routes.users import users_bp
def assign_classgroup_from_dob(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if 2 <= age <= 6:
        return ClassGroup.query.filter_by(name="2-6").first()
    elif 7 <= age <= 12:
        return ClassGroup.query.filter_by(name="7-12").first()
    else:
        return ClassGroup.query.filter_by(name="Teens").first()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'

db.init_app(app)
migrate = Migrate(app, db)

# BLUEPRINT REGISTRATION.
# Class groups and session routes are modlurized into
# separate blueprints foir cleaner structure.
app.register_blueprint(classgroups_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(users_bp)

# DASHBOARD ROUTE (Main Landing Page).
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Dashboard will eventually show stats, quick links, etc. 
    return render_template('dashboard.html')

# USER PAGE - List All Users.
@app.route('/users')
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


# DELETE USER - Utility Route.
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

# ATTENDANCE RECORDS PAGE.
@app.route('/attendance')
def attendance():
    records = AttendanceRecord.query.all()
    return render_template('attendance.html', records=records)

# AUTOCOMPLETE USERS SEARCH.
@app.route("/users/search")
def search_users():
    q = request.args.get("q", "")
    users = User.query.filter(User.full_name.ilike(f"%{q}%")).all()
    return jsonify([u.to_dict() for u in users])

# APP RUNNER.
if __name__ == '__main__':
    app.run(debug=True)