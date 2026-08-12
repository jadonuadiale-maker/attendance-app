from extensions import db
from models import User, ClassGroup
from app import app
from datetime import date

with app.app_context():

    # -----------------------------
    # 1. ADMIN ACCOUNT
    # -----------------------------
    admin = User(
        first_name="System",
        surname="Admin",
        full_name="System Admin",
        date_joined=date(2026, 7, 13),
        role="admin"
    )
    admin.set_password("admin123")
    db.session.add(admin)

    # -----------------------------
    # 2. CLASSGROUP CREATION
    # -----------------------------
    groups = {
        "2-6": None,
        "7-12": None,
        "Teens": None
    }

    for name in groups.keys():
        group = ClassGroup.query.filter_by(name=name).first()
        if not group:
            group = ClassGroup(name=name, is_active=True)
            db.session.add(group)
            db.session.commit()
        groups[name] = group

    # -----------------------------
    # 3. PAD ACCOUNTS (REPLACE TEACHERS)
    # -----------------------------
    pad_2_6 = User(
        first_name="Pad",
        surname="2-6",
        full_name="Pad 2-6",
        date_joined=date.today(),
        role="pad",
        classgroup_id=groups["2-6"].id
    )
    pad_2_6.set_password("pad123")
    db.session.add(pad_2_6)

    pad_7_12 = User(
        first_name="Pad",
        surname="7-12",
        full_name="Pad 7-12",
        date_joined=date.today(),
        role="pad",
        classgroup_id=groups["7-12"].id
    )
    pad_7_12.set_password("pad123")
    db.session.add(pad_7_12)

    pad_teens = User(
        first_name="Pad",
        surname="Teens",
        full_name="Pad Teens",
        date_joined=date.today(),
        role="pad",
        classgroup_id=groups["Teens"].id
    )
    pad_teens.set_password("pad123")
    db.session.add(pad_teens)

    # -----------------------------
    # FINAL COMMIT
    # -----------------------------
    db.session.commit()
    print("Seeded admin and pad users for all classgroups.")