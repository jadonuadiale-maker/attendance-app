from datetime import datetime, timedelta
from models import ClassGroup, Session
from extensions import db

def auto_create_sessions(mode="daily"):
    today = datetime.now().date()       # Capture today's date once — avoids repeated datetime calls.
    groups = ClassGroup.query.all()     # Auto‑creation runs per class group.
    created = []                        # Track newly created sessions for API return + debugging.

    for group in groups:
        schedule_days = ["Sunday"]      # Placeholder schedule — later stored per ClassGroup.
        weekday = today.strftime("%A")  # Convert date → weekday name (e.g., "Sunday").

        if weekday not in schedule_days:
            continue                # Skip groups not scheduled today.

        existing = Session.query.filter_by(
            classgroup_id=group.id,
            date=str(today)
        ).first()                   # Prevent duplicate sessions for the same day.

        if existing:
            continue

        session = Session(
            classgroup_id=group.id,
            date=str(today),
            topic="Auto‑generated session"
        )
        db.session.add(session)
        created.append(session)

        for s in created:
            assert s.classgroup_id is not None # Ensure session is linked to a group.
            assert ClassGroup.query.get(s.classgroup_id) # Ensure referenced group exists. 

    db.session.commit()     # Commit all staged sessions in one transaction.

    return created          # Return raw objects for internal use. 
