# Bolg Application

## Overview
A Django-based blog platform that allows users to create and manage blog posts.

## Features
- User authentication and registration
- Create, read, update, and delete blog posts
- Comments system
- Search functionality
- Responsive design

## Technology Stack
- Python 3.x
- Django 4.x
- SQLite (development)
- HTML/CSS/JavaScript
- Celery for background tasks

## Installation

### Prerequisites
- Python 3.x
- pip package manager
- Virtual environment (recommended)

### Setup
1. Clone the repository
```bash
git clone https://github.com/your-username/Bolg_Application.git
cd Bolg_Application
```

2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv myvenv

# Activate on Windows
myvenv\Scripts\activate

# Activate on macOS/Linux
source myvenv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run database migrations
```bash
python manage.py migrate
```

5. Create admin user
```bash
python manage.py createsuperuser
```

6. Start development server
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Usage
- Admin panel: http://127.0.0.1:8000/admin/
- Home page: http://127.0.0.1:8000/

## Project Structure
```
Bolg_Application/
├── bolg_project/         # Main project settings
├── mainapp/              # Main blog application
├── utils/                # Utility functions and Celery tasks
├── media/                # User uploaded files
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Development
- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Write tests for new features

## Deployment
Deployment instructions for various platforms:

### Heroku
```bash
# Install Heroku CLI
# Add Procfile
# Configure environment variables
heroku create
git push heroku main
```



