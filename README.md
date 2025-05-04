# MediHub - Smart Hospital & Health Management System

MediHub is a Django-based system built to simplify healthcare management in Rwanda. It helps hospitals organize their services better and supports patients—especially those with chronic illnesses—by tracking their health data and medication schedules.

## Purpose

MediHub aims to solve real-life problems such as:

- Patients forgetting to take medication or track symptoms.
- Doctors lacking updated patient logs during appointments.
- Hospitals struggling with disorganized patient data and communication.

This system brings doctors, patients, and administrators into one platform for better collaboration and service delivery.

## Features

- User Authentication (Patients, Doctors, Admin)
- Doctor Dashboard: View patient logs, notes, appointments
- Patient Panel: Log daily vitals (blood pressure, sugar, symptoms), get reminders
- Appointment Management: Request and approval system
- Communication: Chat and notes between doctors and patients
- Reports: Health logs visualized using charts (Chart.js)
- Reminders: Daily alerts for medication using Celery Beat
- Admin Interface: Full control of users and data

## Technologies Used

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap or Tailwind
- Database: SQLite (Development)
- Async Tasks: Django Celery + Celery Beat
- Charts: Chart.js

## Setup Instructions (Local Development)

1. Clone the Repository:
 https://github.com/Annithah/MediHub_System.git

