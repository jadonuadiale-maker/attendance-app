from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from datetime import date
from extensions import db
from models import *
from routes.classgroups import classgroups_bp
from routes.sessions import sessions_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'

db.init_app(app)
migrate = Migrate(app, db)

# BLUEPRINT REGISTRATION.
# Class groups and session routes are modlurized into
# separate blueprints foir cleaner structure.
app.register_blueprint(classgroups_bp)
app.register_blueprint(sessions_bp)

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
    name = request.form['username']
    user = User(name=name)
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

# APP RUNNER.
if __name__ == '__main__':
    app.run(debug=True)