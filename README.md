# CampusConnect

CampusConnect is a Django web platform for college students to communicate, discover opportunities, and help each other on campus.

## Features

- Secure signup, login, logout, and student profiles
- Community-based posts with optional image uploads
- Local ML-powered post categorization (Academic, Placement, Event, Marketplace, Lost & Found, or General)
- Likes, comments, edit/delete controls, and post reporting
- Events page with event creation and RSVP tracking
- Lost & Found board with photos and locations
- Global search across posts, communities, and events
- In-app notifications for likes, comments, and RSVPs
- Django admin panel for moderation and management

## Technology

- Python 3
- Django 6
- SQLite during development
- Bootstrap 5 for the responsive interface
- Pillow for image uploads
- scikit-learn for the local text classifier

## Run locally

```powershell
git clone <your-repository-url>
cd campusconnect
python -m venv venv
venv\Scripts\activate
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Run tests

```powershell
python manage.py test
```

## Important pages

- `/` — campus feed
- `/communities/` — community discovery
- `/events/` — events and RSVPs
- `/lost-found/` — lost and found board
- `/search/` — global search
- `/notifications/` — student activity
- `/admin/` — administration and moderation

## Future improvements

- College-email verification
- Direct messaging between students
- Email notifications
- Deployment with PostgreSQL and cloud image storage
