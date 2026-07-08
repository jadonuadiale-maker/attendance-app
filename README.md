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

Teachers and admins can:
- view today’s session instantly  
- see who has checked in  
- manually mark late arrivals or absences  
- delete or modify sessions in exceptional cases (e.g., class cancelled, combined service)  

This replaces the need for teachers to send attendance updates in group chats.

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

# 🧱 System Architecture (High‑Level)

## Models

### User
- first_name  
- surname  
- full_name (auto‑generated)  
- date_of_birth  
- classgroup_id (auto‑assigned based on age)  
- date_joined  
- role (admin / teacher / member)

### ClassGroup
- name (2–6, 7–12, Teens)  
- description  
- relationships to users and sessions  

### Session
- classgroup_id  
- date (Sunday)  
- topic (shared across both services)  
- auto‑created weekly  
- editable by admin/teacher  

### AttendanceRecord
- user_id  
- session_id  
- service_number (1 or 2 or both)  
- status (present / absent / late)  
- timestamp  

This structure allows unlimited scalability and clean analytics.

# 🖥️ Tech Stack
- Backend: Flask  
- Database: SQLAlchemy (SQLite for dev)  
- Frontend: HTML, Bootstrap  
- Templating: Jinja2  
- Version Control: Git + GitHub  

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
