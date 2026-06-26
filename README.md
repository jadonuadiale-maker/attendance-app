# 📌 Overview
The Attendance App is a scalable attendance‑tracking system designed for churches and multi‑group organisations.
It solves the challenges of manual attendance recording, inconsistent tracking, and lack of centralised reporting by providing an automated, structured, and role‑based attendance management platform.

This project is part of my Summer Mastery Framework (SMF) and represents the foundation month’s capstone system before moving into full‑scale development.

# 🎯 Purpose
## 📲 How the App Improves the Current Attendance Workflow
Church attendance today is often recorded manually on paper. Members write their names beside the service they attend, newcomers add their details at the bottom of the sheet, and teachers later send attendance updates in group chats. This process is familiar, but slow, inconsistent, and requires repeated manual entry.

The Attendance App modernises this workflow while keeping the core structure intact.

## 🧍‍♂️ Existing Members — Fast Digital Check‑In
Instead of writing their names on paper, existing members check in using a tablet or iPad at the door.

- They type the first few letters of their name
- The system autocompletes from the database
- They select their profile
- They mark whether they are attending 1st service or 2nd service
- Their attendance is instantly recorded for the current session 
- This mirrors the current process but removes handwriting, errors, and manual updates.

## 🆕 Newcomers — Seamless Onboarding
Newcomers no longer write their details at the bottom of a sheet.

- They tap “New Member”
- Enter their basic information
- They are automatically added to the correct class group
- Their attendance for that day is recorded immediately
- This eliminates the need for later data entry.

## 🗓️ Sessions — Automated but Editable
The system automatically creates sessions for each class group based on the service schedule.
Teachers and admins can:

- view today’s session instantly
- see who has checked in
- manually mark late arrivals or absences
- delete or modify sessions in exceptional cases (e.g., class cancelled, combined service)
- This replaces the need for teachers to send attendance updates in group chats.

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