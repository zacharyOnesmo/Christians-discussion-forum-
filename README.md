# Neno Lens

Neno Lens is an evidence-first Christian claim investigation platform designed to help users explore theological questions with structure and critical thinking, not a simple yes/no answer.

The system is built primarily for Swahili users, with English support available, and it encourages investigation across multiple layers:

- Biblical text
- Biblical context
- Historical interpretation
- Scholarly and research evidence
- Modern technology facts
- Personal interpretation
- Speculation and unsupported claims

This project is a Django web application focused on user accounts, claim analysis, investigation history, and localized experience.

## Features

- Swahili-first interface with English toggle
- User registration and login
- Personalized profile dashboard
- Claim submission and investigation workflow
- Detailed claim pages with evidence breakdowns
- User-specific claim history
- Evidence-driven output instead of binary true/false conclusions
- Premium dark-theme UI with responsive dashboard layout
- CSRF-safe setup for local preview/dev environments

## Technology Stack

- Python 3
- Django 6.1.1
- SQLite (development database)
- HTML, CSS, JavaScript
- Django authentication system

## Project Structure

```text
.
├── dashboard/
│   ├── static/dashboard/
│   ├── templates/dashboard/
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── neno_lens/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3
├── README.md
└── .venv/
```

## Main App Flow

1. User creates an account or logs in.
2. User submits a claim or question for investigation.
3. The app organizes the claim into analysis categories.
4. The system summarizes findings across evidence layers.
5. The user can review their submission history in the profile area.
6. Each claim has its own detail page for deeper investigation context.

## Local Setup

```bash
cd /workspaces/Christians-discussion-forum-
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

Then open the local Django app in your browser:

- http://localhost:8000/

## Demo / Seed Data

The application includes logic to create demo content when the database is empty, while user-submitted claims are linked to the authenticated user account.

## Language Support

The app supports both:

- Swahili (default)
- English

The current language is stored in the session and can be switched from the interface.

## Tests

Run the project test suite with:

```bash
python manage.py test dashboard
```

## Notes

This is a working Django project intended for product-style demo and development use, with a focus on Christian claim analysis, evidence separation, and structured investigation rather than simplistic verdicts.

## License

This project is currently intended for local development and educational/demo usage unless a specific license is added later.
