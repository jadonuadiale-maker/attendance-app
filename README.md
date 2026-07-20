# 📌 Overview
The Attendance App is a scalable attendance‑tracking system designed for churches and multi‑group organisations.
It solves the challenges of manual attendance recording, inconsistent tracking, and lack of centralised reporting by providing an automated, structured, and role‑based attendance management platform.

This project is part of my Summer Mastery Framework (SMF) and represents the foundation month’s capstone system before moving into full‑scale development.

# 🎯 Purpose

## 📲 How the App Improves the Current Attendance Workflow
Church attendance today is often recorded manually on paper. Members write their names beside the service they attend, newcomers add their details at the bottom of the sheet, and teachers later send attendance updates in group chats. This process is familiar, but slow, inconsistent, and requires repeated manual entry.

The Attendance App modernises this workflow while keeping the core structure intact.

## 🧍‍♂️ Existing Members — Fast Digital Check‑In
Existing members check in using a tablet or iPad at the door.

- All users are displayed alphabetically by full name  
- Members can tap their name directly or type the first few letters  
- They select whether they are attending 1st service, 2nd service, or both  
- Their attendance is instantly recorded for the correct class group session  
- Check‑in opens at 08:45 to accommodate early arrivals  

This mirrors the current paper workflow but removes handwriting, errors, and manual updates.

## 🆕 Newcomers — Seamless Onboarding
Newcomers tap the “First Timer” card.

They enter:
- First name  
- Surname  
- Date of birth  

The system automatically:
- assigns the correct class group based on age  
- creates their user profile  
- records their attendance for today  
- stores their date_joined automatically  

This eliminates manual onboarding and ensures newcomers are immediately included in attendance records.

## 🗓️ Sessions — Automated but Editable
Every Sunday consists of two services:

- 1st Service: 09:00–10:40  
- 2nd Service: 10:45–12:30  

The church runs three class groups:
- 2–6  
- 7–12  
- Teens  

The system automatically creates one session per class group per Sunday.  
Each session contains attendance for Service 1, Service 2, or both, depending on what the member selects during check‑in.

## 👩‍🏫 Teacher & Admin Control
Although the system automates most of the workflow, teachers and admins retain full control:

- override attendance  
- correct mistakes  
- delete sessions  
- add special sessions  
- update class group membership  

Automation handles the routine; humans handle the exceptions.

## 📈 Why This Matters
This design:

- mirrors the familiar paper workflow  
- removes double entry  
- reduces errors  
- speeds up check‑in  
- centralises attendance data  
- supports real‑time dashboards  
- scales across ministries and campuses  

It is a direct technological evolution of the current system — not a replacement of the workflow, but an upgrade of it.

# 🖥️ Tech Stack
- Backend: Flask  
- Database: SQLAlchemy + Flask-Migrate (SQLite for dev)  
- Frontend: HTML, Bootstrap  
- Templating: Jinja2  
- Version Control: Git + GitHub  

# Setup Instructions
### Environment Variables
Create a `.env` file or set environment variables:
`SECRET-KEY=your_secret_key`
`DATABASE_URL=sqlite:///attendance.db`
### Running the App
```flask run``` or ```python app.py```
### Database Migrations
Initialise migrations:
```flask db init```
Create migrations:
```flask db migrate -m "initial tables"```
Apply migration:
```flask db upgrade```
### Seeding Admin + Teacher
```python seed.py```
This creates:
- Admin user (System Admin)
- Teacher user (John Doe, assigned to classgroup_id=1)

# System Architecture

## Models
### User
Fields:
- first_name
- surname
- full_name
- date_of_birth
- date_joined
- classgroup_id
- password_hash
- role(admin, teacher, member)
Relationships:
- belongs to ClassGroup
- has many AttendanceRecords
### ClassGroup
Fields:
- id
- name
Relationships:
- has many Sessions
- has many Users
### Session
Fields:
- id
- classgroup_id
- date 
- topic
- description
Constraints: 
- unique (classgroup_id, date)
### AttendanceRecord
Fields:
- id
- user_id
- session_id
- date
- status (present, absent, late)
- service_number (1, 2, 3 for both)

## Architecture Notes
### Session Logic
- Auto-creation runs daily or manually via `/sessions/auto_create`.
- Prevents duplicates using technique constraint and query checks. 
- Sessions are tied to class groups.
- Check‑in pads only work for today’s sessions.
- Teachers can only view sessions for their assigned class group.
- Duplicate check‑ins are rejected.
- Admins can override attendance status and service number.
### RBAC(Role-Based Access Control)
Roles: 
- admin
- teacher
- member
Mechanics: 
- Login stores `user_id` and `role`in session. 
- `login_required` protects all internal pages. 
- `role-required` restricts admin/teacher pages. 
- Teachers are scoped to their class group in sessions and attendance views. 
### Attendance Flow
- Members select service number (1, 2, 3).
- Duplicate check-ins are blocked. 
- First timer create a profile and are auto-assigned to a class group based on DOB.
- Attendance is stored in the correct session for today. 
- Admin override allows fixing mistakes. 
- Attendance marking page allows manual updates. 
### Reports System
Reports include: 
#### Weekly 
- service loads
- late
- absent
- both services
- class group filters
#### Monthly
- service loads
- late 
- absent
- class group filters
#### Yearly 
- first timers
- service loads
- late 
- absent
#### Retention
- users absent for N weeks
- class group filters
#### First Timers
- users whose date_joined == attendance date
#### Operations
- raw attendance for a specific date/service/classgroup

## API Routes
### Auth 
- GET `/login`
- POST `/login`
- GET `/logout`
### Users
- GET `/users`
- GET `/users/search`
- GET `/users/search_by_group`
- GET `/first_timer/<session_id>`
- POST `/first_timer/submit`
- GET `/admin/users/create`
- POST `/admin/users/submit`
### ClassGroups
- GET `/classgroups` 
- POST `/classgroups`  
- GET `/classgroups/<id>`  
- DELETE `/classgroups/<id>`  
- GET `/classes/view`  
- GET `/classes`
### Sessions
- GET `/sessions`  
- GET `/sessions/view`  
- GET `/classgroups/<id>/sessions`  
- POST `/classgroups/<id>/sessions`  
- POST `/sessions/create`  
- GET `/sessions/<id>/view`  
- GET `/sessions/<id>`  
- GET `/sessions/<id>/checkin/view`  
- GET `/checkin/<user_id>/<session_id>`  
- POST `/sessions/<session_id>/checkin`  
- POST `/checkin/submit`  
- POST `/attendance/<record_id>/override`  
- GET `/sessions/<id>/attendance/view`  
- GET `/sessions/auto_create`
### Reports 
- GET `/reports/weekly`  
- GET `/reports/monthly`  
- GET `/reports/yearly`  
- GET `/reports/retention`  
- GET `/reports/first_timers`  
- GET `/reports/operations`

## Screenshots
Recommended screenshots(sort this later...):
Dashboard
Class groups page
Sessions page
Check‑in pad
Check‑in detail
First timer flow
Attendance marking
Weekly report
Monthly report
Yearly report
Retention report
First timers report
Operations report

# 🚀 Core Features (Current + Planned)

## ✅ Current Foundation Features
- Flask backend  
- SQLAlchemy models  
- Basic attendance submission  
- Simple templates with Bootstrap  
- Basic routing and page structure  

## 🏗️ Planned Features (Month 2 MVP)

### Sessions System
- One session per class group per Sunday  
- Attendance tracked per service (1st, 2nd, or both)  
- Teachers/admins can edit or override attendance  

### Class Groups
- 2–6  
- 7–12  
- Teens  
- Adults  
- Departments (ushers, choir, media, etc.)

### Role‑Based Access
- Admin  
- Teacher  
- Member  

### Attendance Dashboard
- View attendance by class  
- View attendance by date  
- Member attendance history  
- Teacher session reports  

### Scalability
- Multiple classes  
- Multiple teachers  
- Unlimited sessions  
- Clean relational database design  

## Project Reset (June 30 2026)
This version begins the structured rebuild of the Attendance App.  
- Focus: Flask routing layer (ClassGroups, Sessions, AttendanceRecords)  
Legacy prototype archived in branch: `prototype-v1`.

# 📅 Development Roadmap

## Month 1 (Foundation) — Completed
- Flask basics  
- Routing  
- Templates  
- Database setup  
- Basic attendance flow  

## Month 2 (Real Building) — Upcoming
- Authentication  
- Roles  
- Sessions  
- Class groups  
- Dashboards  
- Analytics  
- Deployment  

# 📌 Vision
The long‑term goal is to build a full church operations tool that can:

- track attendance  
- analyse engagement  
- support multiple ministries  
- provide leadership insights  
- scale across campuses  
