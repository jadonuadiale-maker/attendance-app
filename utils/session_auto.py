from datetime import datetime, timedelta
from models import ClassGroup, Session
from extensions import db
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.INFO)

def auto_create_sessions(mode="daily"):
    today = datetime.now().date()       # Capture today's date once — avoids repeated datetime calls.
    groups = ClassGroup.query.all()     # Auto‑creation runs per class group.
    created = []                        # Track newly created sessions for API return + debugging.

    logging.info(f"Auto-create triggered at {datetime.now()} for {len(groups)} groups.")

    for group in groups:
        schedule_days = ["Sunday", "Friday"]      # Placeholder schedule — later stored per ClassGroup.
        weekday = today.strftime("%A")  # Convert date → weekday name (e.g., "Sunday").

        if weekday not in schedule_days:
            continue                # Skip groups not scheduled today.

        existing = Session.query.filter_by(
            classgroup_id=group.id,
            date=today
        ).first()                   # Prevent duplicate sessions for the same day.

        if existing:
            continue

        session = Session(
            classgroup_id=group.id,
            date=today,
            topic="Auto‑generated session",
            start_time=datetime.strptime("09:00", "%H:%M").time(),      # Default service times. 
            end_time=datetime.strptime("12:30", "%H:%M").time()
        )

        db.session.add(session)
        created.append(session)

        for s in created:
            assert s.classgroup_id is not None # Ensure session is linked to a group.
            assert ClassGroup.query.get(s.classgroup_id) # Ensure referenced group exists. 

    db.session.commit()     # Commit all staged sessions in one transaction.

    return created          # Return raw objects for internal use. 
