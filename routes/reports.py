# routes/reports.py
from flask import Blueprint, render_template, request
from datetime import date, datetime, timedelta
from extensions import db
from models import AttendanceRecord, Session, User, ClassGroup
from utils.auth_utils import login_required, role_required

reports_bp = Blueprint("reports", __name__)

# Helper: parse date safely from query params.
def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

# WEEKLY REPORT.
@reports_bp.route("/reports/weekly")
@login_required
@role_required("admin", "teacher")
def weekly_health_report():
    # Filters: optional classgroup_id, week_start, week_end
    classgroup_id = request.args.get("classgroup_id", type=int)
    week_start = parse_date(request.args.get("week_start"))
    week_end = parse_date(request.args.get("week_end"))

    # Default: current week (Mon–Sun)
    today = date.today()
    if not week_start or not week_end:
        week_start = today
        week_end = today

    # Base query: attendance within date range
    query = AttendanceRecord.query.filter(
        AttendanceRecord.date >= week_start,
        AttendanceRecord.date <= week_end
    )

    # Optional filter by class group via Session
    if classgroup_id:
        query = query.join(Session).filter(Session.classgroup_id == classgroup_id)

    records = query.join(User).filter(User.role == "member").all()

    # Metrics
    total = len(records)
    # Raw categories.
    service1 = sum(1 for r in records if r.service_number == 1)
    service2 = sum(1 for r in records if r.service_number == 2)
    both = sum(1 for r in records if r.service_number == 3)

    # Correct service loads. 
    service1_load = service1 + both
    service2_load = service2 + both

    late = sum(1 for r in records if r.status == "late")
    absent = sum(1 for r in records if r.status == "absent")

    report = {
        "title": "Weekly Health Report",
        "filters": {
            "classgroup_id": classgroup_id,
            "week_start": week_start,
            "week_end": week_end,
        },
        "metrics": {
            "total": total,
            "service1": service1,
            "service2": service2,
            "both": both,
            "late": late,
            "absent": absent,
            "service1_load": service1_load,
            "service2_load": service2_load,
        },
        "records": records,
        "time_scope": {
            "start": week_start,
            "end": week_end,
        },
    }

    # Class groups for filter dropdown
    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="weekly")

# MONTHLY REPORT.
@reports_bp.route("/reports/monthly")
@login_required
@role_required("admin", "teacher")
def monthly_trends_report():
    # Filters: month, year, optional classgroup_id
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    classgroup_id = request.args.get("classgroup_id", type=int)

    today = date.today()
    month = month or today.month
    year = year or today.year

    query = AttendanceRecord.query.filter(
        db.extract("month", AttendanceRecord.date) == month,
        db.extract("year", AttendanceRecord.date) == year
    )

    if classgroup_id:
        query = query.join(Session).filter(Session.classgroup_id == classgroup_id)

    records = query.join(User).filter(User.role == "member").all()

    total = len(records)
    # Raw categories. 
    service1 = sum(1 for r in records if r.service_number == 1)
    service2 = sum(1 for r in records if r.service_number == 2)
    both = sum(1 for r in records if r.service_number == 3)
    
    # Correct service loads. 
    service1_load = service1 + both
    service2_load = service2 + both

    late = sum(1 for r in records if r.status == "late")
    absent = sum(1 for r in records if r.status == "absent")

    report = {
        "title": "Monthly Trends Report",
        "filters": {
            "classgroup_id": classgroup_id,
            "month": month,
            "year": year,
        },
        "metrics": {
            "total": total,
            "service1": service1,
            "service2": service2,
            "both": both,
            "late": late,
            "absent": absent,
            "service1_load": service1_load,
            "service2_load": service2_load,
        },
        "records": records,
        "time_scope": {
            "month": month,
            "year": year,
        },
    }

    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="monthly")

# ANNUAL REPORTS. 
@reports_bp.route("/reports/yearly")
@login_required
@role_required("admin", "teacher")
def yearly_growth_report():
    # Filters: year, optional classgroup_id
    year = request.args.get("year", type=int)
    classgroup_id = request.args.get("classgroup_id", type=int)

    today = date.today()
    year = year or today.year

    query = AttendanceRecord.query.filter(
        db.extract("year", AttendanceRecord.date) == year
    )

    if classgroup_id:
        query = query.join(Session).filter(Session.classgroup_id == classgroup_id)

    records = query.join(User).filter(User.role == "member").all()

    total = len(records)
    # Raw categories.
    service1 = sum(1 for r in records if r.service_number == 1)
    service2 = sum(1 for r in records if r.service_number == 2)
    both = sum(1 for r in records if r.service_number == 3)

    # Correct service loads.
    service1_load = service1 + both
    service2_load = service2 + both

    late = sum(1 for r in records if r.status == "late")
    absent = sum(1 for r in records if r.status == "absent")

    # First timers: date_joined == attendance date
    first_timers = [
        r for r in records
        if r.user and r.user.date_joined == r.date
    ]

    report = {
        "title": "Yearly Growth Report",
        "filters": {
            "classgroup_id": classgroup_id,
            "year": year,
        },
        "metrics": {
            "total": total,
            "service1": service1,
            "service2": service2,
            "both": both,
            "late": late,
            "absent": absent,
            "first_timers": len(first_timers),
            "service1_load": service1_load,
            "service2_load": service2_load,
        },
        "records": records,
        "time_scope": {
            "year": year,
        },
    }

    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="yearly")

# RETENTION REPORTS.
@reports_bp.route("/reports/retention")
@login_required
@role_required("admin", "teacher")
def retention_report():
    # Filters: weeks_absent, optional classgroup_id
    weeks_absent = request.args.get("weeks_absent", type=int) or 4
    classgroup_id = request.args.get("classgroup_id", type=int)

    cutoff_date = date.today() - timedelta(weeks=weeks_absent)

    # Users with no attendance since cutoff_date
    # Simple version: users whose latest attendance is before cutoff_date
    users = User.query.filter_by(role="member").all()
    drifting = []

    for u in users:
        last_record = (
            AttendanceRecord.query
            .filter_by(user_id=u.id)
            .order_by(AttendanceRecord.date.desc())
            .first()
        )
        if not last_record or last_record.date < cutoff_date:
            if classgroup_id and u.classgroup_id != classgroup_id:
                continue
            drifting.append(u)

    report = {
        "title": "Retention Report",
        "filters": {
            "weeks_absent": weeks_absent,
            "classgroup_id": classgroup_id,
        },
        "metrics": {
            "drifting_count": len(drifting),
        },
        "records": drifting,
        "time_scope": {
            "cutoff_date": cutoff_date,
        },
    }

    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="retention")

# FIRST TIMERS REPORT. 
@reports_bp.route("/reports/first_timers")
@login_required
@role_required("admin", "teacher")
def first_timers_report():
    # Filters: month/year or week, optional classgroup_id
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    classgroup_id = request.args.get("classgroup_id", type=int)

    today = date.today()
    month = month or today.month
    year = year or today.year

    # Attendance in month/year where user.date_joined == attendance date
    query = AttendanceRecord.query.filter(
        db.extract("month", AttendanceRecord.date) == month,
        db.extract("year", AttendanceRecord.date) == year
    ).join(User)

    if classgroup_id:
        query = query.join(Session).filter(Session.classgroup_id == classgroup_id)

    records = query.join(User).filter(User.role == "member").all()
    first_timers = [
        r for r in records
        if r.user and r.user.date_joined == r.date
    ]

    report = {
        "title": "First Timers Report",
        "filters": {
            "classgroup_id": classgroup_id,
            "month": month,
            "year": year,
        },
        "metrics": {
            "first_timers": len(first_timers),
        },
        "records": first_timers,
        "time_scope": {
            "month": month,
            "year": year,
        },
    }

    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="first_timers")

# OPERATIONS REPORT.
@reports_bp.route("/reports/operations")
@login_required
@role_required("admin", "teacher")
def operations_report():
    # Filters: classgroup_id, date, service_number
    classgroup_id = request.args.get("classgroup_id", type=int)
    report_date = parse_date(request.args.get("date"))
    service_number = request.args.get("service_number", type=int)

    query = AttendanceRecord.query

    if report_date:
        query = query.filter(AttendanceRecord.date == report_date)

    if service_number:
        query = query.filter(AttendanceRecord.service_number == service_number)

    if classgroup_id:
        query = query.join(Session).filter(Session.classgroup_id == classgroup_id)

    records = query.join(User).filter(User.role == "member").all()      # Only members attendance are recorded. 

    total = len(records)

    report = {
        "title": "Operational Report",
        "filters": {
            "classgroup_id": classgroup_id,
            "date": report_date,
            "service_number": service_number,
        },
        "metrics": {
            "total": total,
        },
        "records": records,
        "time_scope": {
            "date": report_date,
        },
    }

    groups = ClassGroup.query.all()
    return render_template("reports.html", report=report, groups=groups, active_tab="operations")