from extensions import db
from models import User
from app import app
from datetime import date

with app.app_context():
    # Create an admin user
    admin = User(
        first_name="System",
        surname="Admin",
        full_name="System Admin",
        date_joined=date(2026, 7, 13),
        role="admin"
    )
    admin.set_password("admin123")  # secure hash stored, not plain text
    db.session.add(admin)

    # Create a teacher user
    teacher = User(
        first_name="John",
        surname="Doe",
        full_name="John Doe",
        date_joined=date(2026, 7, 13),
        role="teacher"
    )
    teacher.set_password("teacher123")
    db.session.add(teacher)

    db.session.commit()
    print("Seeded admin and teacher users.")
