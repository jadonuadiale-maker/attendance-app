# Attendance App API Endpoints
This document describes all available endpoints for managing class groups and sessions. 
Base URL: `http://127.0.0.1:5000`

## ClassGroups
| Method | Endpoint | Description | Request Body | Response |
|---------|-----------|--------------|---------------|-----------|
| GET | /classgroups | Get all class groups | — | List of class groups |
| POST | /classgroups | Create a class group | {"name": "Teens"} | Created group |
| GET | /classgroups/`<id>` | Get single class group | — | Group details |
| DELETE | /classgroups/`<id>` | Delete class group | — | {"message": "Deleted"} |

## Sessions
| Method | Endpoint | Description | Request Body | Response |
|---------|-----------|--------------|---------------|-----------|
| GET | /classgroups/<group_id>/sessions | Get all sessions for a group | — | List of sessions |
| POST | /classgroups/<group_id>/sessions | Create a session | {"date": "2026-06-30", "topic": "Intro"} | Created session |
| GET | /sessions/<id> | Get single session | — | Session details |
