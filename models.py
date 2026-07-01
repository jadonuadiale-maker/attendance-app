from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class ClassGroup(db.Model):
    __tablename__ = "classgroups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship: a class group has many sessions. 
    sessions = db.relationship("Session", backref="classgroup", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    classgroup_id = db.Column(db.Integer, db.ForeignKey("classgroups.id"), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "classgroup_id": self.classgroup_id,
            "date": self.date,
            "topic": self.topic
        }
class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)