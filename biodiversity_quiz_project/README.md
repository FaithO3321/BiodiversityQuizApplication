# Biodiversity Conservation Interactive Quiz Application

## Overview
This project is an interactive quiz application that allows users to answer multiple-choice questions related to **biodiversity conservation**. It tracks quiz results under user accounts and includes features such as scoring, time limits, social media sharing, and REST API exposure. 

This project is built using **Django** for the backend, **MySQL** for database storage, and **HTML/CSS** for the frontend.

---

## Features
- **User Authentication**: Secure registration, login, and session management for users.
- **Quiz System**: Multiple-choice questions with scoring, time limits, and feedback.
- **Responsive Design**: Mobile-friendly UI for an optimal experience across devices.
- **Quiz Results Storage**: User-specific results stored in the database.
- **REST API**: Endpoints for accessing quizzes and questions.
- **Error Handling**: Custom error pages and API exception handling.
- **Social Sharing**: Share quiz results to popular social media platforms.
- **Caching**: Improve performance by caching quiz data using Redis.
- **Pagination**: Efficient pagination of quizzes and results for large datasets.

---

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: MySQL
- **Caching**: Redis (for caching quiz data)
- **Testing**: Django Test Framework
- **REST API**: Django REST Framework

---

## Project Structure
The project structure is included in the file Project_Structure

---

## Installation and Setup

### Step 1: Prerequisites
Ensure you have the following installed:
- Python 3.8+
- MySQL
- Redis (for caching)
- Git (for version control)
- Optional: Docker for containerized development setup

### Step 2: Clone the Repository
```bash
git clone https://github.com/your-username/BiodiversityQuizApplication.git
cd BiodiversityQuizApplication
### Step 3: Create and Activate Virtual Environment
- use the following commands:
- python3 -m venv quiz_env
- source quiz_env/bin/activate

### Step 4: Install Dependencies
- **pip install -r requirements.txt

### Step 5: Configure MySQL Database
Install MySQL and create a new database.
Update the DATABASES settings in biodiversity_quiz_project/settings.py

### Step 6: Run Database Migrations
python manage.py makemigrations
python manage.py migrate

### Step 7: Load Initial Quiz Data
python manage.py loaddata data/biodiversity_questions.json

### Step 8: Create a Superuser for Admin Access
python manage.py createsuperuser

### Step 9: Run the Development Server

python manage.py runserver

# API Endpoints
The REST API exposes the following endpoints for external integrations:

/api/quizzes/: List all quizzes (GET) and create a new quiz (POST).
/api/quizzes/<int:id>/: Retrieve, update, or delete a specific quiz (GET, PUT, DELETE).
/api/questions/: List all questions (GET) and create a new question (POST).
/api/questions/<int:id>/: Retrieve, update, or delete a specific question (GET, PUT, DELETE).
/api/results/: List all quiz results (GET) and submit a new result (POST).


# Error Handling
Custom error pages and exception handling are implemented for better user experience and API robustness:

404 Error: A custom page is displayed when a user navigates to a non-existent page.
500 Error: A friendly error page is displayed in case of server errors.
API Errors: Django REST Framework's exception_handler handles API errors gracefully.

# Social Sharing
Users can share their quiz results on social media platforms. The system uses Open Graph meta tags to ensure that shared content is optimized for social media previews.

# Caching 
Caching is used to enhance the performance of frequently accessed quiz data. The project uses Redis as the caching backend.

# Pagination
Django’s Paginator is used for server-side pagination. It is implemented to paginate large quiz lists and quiz results efficiently.

# Testing the Application
##Unit Tests
-Unit tests are written to validate models, views, and API endpoints. To run the tests:
	python manage.py test

##Coverage
To check code coverage:

-Install coverage:
	pip install coverage

- Run the tests with coverage:
	coverage run manage.py test
- View the coverage report:
	coverage report -m
Load Testing
For load testing, tools like Apache JMeter or Locust can be used to simulate multiple users accessing the quiz simultaneously.


