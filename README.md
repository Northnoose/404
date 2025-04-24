# Programming Course

## Description

An interactive web platform designed to teach programming through structured lessons, quizzes, and challenges, aimed at both beginners and users with prior experience.  
The course is module-based, allowing users to progress through levels at their own pace. The platform includes social features such as friend requests, friend search, and the ability to view friends' progress. A scoreboard system ranks users based on points earned through completing tasks and challenges, promoting healthy competition and engagement.

## Getting Started

### Dependencies

- Python 3.x
- Django
- SQLite3 (default with Django)
- A modern web browser
- Git

### Required Python Packages

The necessary packages are listed in `requirements.txt`:

asgiref==3.8.1
Django==5.1.7
djangorestframework==3.15.2
psycopg2==2.9.10
psycopg2-binary==2.9.10
sqlparse==0.5.3
tzdata==2025.1

### Installing

1. Clone the repository:
    bash:
    git clone https://github.com/Northnoose/404.git
   
2. Install required packages in an virtual environment:
    python -m venv venv
    source venv/bin/activate  (Mac/Linux)
    venv\Scripts\activate  (Windows)

    pip install -r requirements.txt

3. Run database migrations:
    python manage.py migrate

4. (Optional) Load fixture for admin user:
    python manage.py loaddata fixtures/admin.json

    Standard admin credentials:

    Username: admin

    Email: admin@epost.no

    Password: Admin404notfound

5. (Optional) Create a superuser manually:
    python manage.py createsuperuser

### Executing Program

    To run the development server:
    python manage.py runserver

    Then open your browser and go to:
    http://127.0.0.1:8000/

## Deployment
    
    The project currently runs locally during development. Deployment to a platform may be considered later.
    
## Help
    
    Common issues and tips:
    - Activate the virtual environment before running commands.
    - Ensure all migrations are applied.

## Contributors

    Project developed by a group of data engineering students, 404 Not Found.

## Lisence

    This project is for educational purposes only and is not intended for commercial use.
