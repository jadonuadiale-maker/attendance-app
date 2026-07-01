from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from datetime import date
from extensions import db
from models import User, AttendanceRecord
from routes.classgroups import classgroups_bp
from routes.sessions import sessions_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db.init_app(app)
app.register_blueprint(classgroups_bp)
app.register_blueprint(sessions_bp)
migarte = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['username']
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/mark/<int:user_id>/<status>')
def mark_attendance(user_id, status):
    record = AttendanceRecord(user_id=user_id, date=date.today(), status=status)
    db.session.add(record)
    db.session.commit()
    return redirect('/attendance')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/attendance')
def attendance():
    records = AttendanceRecord.query.all()
    return render_template('attendance.html', records=records)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/attendance')


if __name__ == '__main__':
    app.run(debug=True)