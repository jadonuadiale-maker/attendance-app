# 📌 Overview
The Attendance App is a scalable attendance‑tracking system designed for churches and multi‑group organisations.
It solves the challenges of manual attendance recording, inconsistent tracking, and lack of centralised reporting by providing an automated, structured, and role‑based attendance management platform.

This project is part of my Summer Mastery Framework (SMF) and represents the foundation month’s capstone system before moving into full‑scale development.

# 🎯 Purpose
Churches often struggle with:

inconsistent attendance records

manual paper‑based tracking

no central dashboard for insights

difficulty managing multiple classes (children, teens, adults)

no way to track trends or member engagement

This app provides a modern, automated solution.

# 🚀 Core Features (Current + Planned)
## ✅ Current Foundation Features
- Flask backend
- SQLAlchemy models
- Basic attendance submission
- Simple templates with Bootstrap
- Basic routing and page structure

## 🏗️ Planned Features (Month 2 MVP)
- Sessions system
   Teachers create sessions for their classes
   Each session tracks attendance separately

- Class Groups
   2–6
   7–12
   Teens
   Adults
   Departments (ushers, choir, media, etc.)

- Role‑based access
   Admin
   Teacher
   Member

- Attendance Dashboard
   View attendance by class
   View attendance by date
   Member attendance history
   Teacher session reports

- Scalability
   Multiple classes
   Multiple teachers
   Unlimited sessions
   Clean relational database design

# 🧱 System Architecture (High‑Level)
## Models
- User
   name, role, class group

- ClassGroup
   e.g., 2–6, 7–12, Teens

- Session
   class group
   teacher
   date/time

- AttendanceRecord
   user
   session
   timestamp

This structure allows unlimited scalability and clean analytics.

# 🖥️ Tech Stack
Backend: Flask
Database: SQLAlchemy (SQLite for dev)
Frontend: HTML, Bootstrap
Templating: Jinja2
Version Control: Git + GitHub

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