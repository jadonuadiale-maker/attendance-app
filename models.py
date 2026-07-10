from extensions import db

# USER MODEL.
# Represents an individual user in the system.
# Currently used by prototype routes for attendance tracking.
# Will later be integrated with class groups or sessions. 
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date)
    date_joined = db.Column(db.Date, nullable=False)

    # NEW - required for class group filtering.
    classgroup_id = db.Column(db.Integer, db.ForeignKey('classgroups.id'), nullable=True)
    classgroup = db.relationship("ClassGroup", backref="users")


    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "surname": self.surname,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "date_joined": self.date_joined.isoformat()
        }

# CLASS GROUP MODEL.
# Represents a group or class(e.g., "Teens").
# Each class group can have multiple sessions. 
class ClassGroup(db.Model):
    __tablename__ = "classgroups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship: one class group -> many sessions. 
    sessions = db.relationship("Session", backref="classgroup", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# SESSION MODEL.
# Represents a single teaching or attendance session.
# Linked to a class group via foreign key.
class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    classgroup_id = db.Column(db.Integer, db.ForeignKey("classgroups.id"), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200))
    description = db.Column(db.String(255))  # Optional field for future expansion. 

    def to_dict(self):
        return {
            "id": self.id,
            "classgroup_id": self.classgroup_id,
            "date": self.date,
            "topic": self.topic,
            "description": self.description
        }

# ATTENDANCE RECORD MODEL.
# Prototype model for tracking attendance per user.
# Will later be linked to sessions instead of just dates.
class AttendanceRecord(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))
    # New field: service_number (1, 2, or 3 for "both")
    service_number = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="attendance_records")
    session = db.relationship("Session", backref="attendance_records")


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "status": self.status,
            "session_id": self.session_id,
            "service_number": self.service_number, # New field in dict. 
        }