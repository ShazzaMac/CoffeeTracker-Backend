Backend README 
-------------------------------------------------------------------

✨ Backend - Cortado | Coffee Tracker ✨

This is the Django REST Framework (DRF) backend for the Cortado Coffee Tracker app. It provides the API services, database models, authentication, OCR processing, and leaderboard logic used by the React frontend.

-------------------------------------------------------------------


✨ Features include ✨

- User registration, login, and password reset

- Submit coffee prices (form or image upload with OCR)

- OCR pipeline using Tesseract, EasyOCR, and Gemini AI

- View café price submissions 

- Leaderboard logic for coffee price guessing game

- Contact form with email + DB storage

- CSRF token handling for secure frontend communication

-------------------------------------------------------------------


✨ Structure ✨

backend/
├── accounts/           # Custom user profiles, signals, and auth logic
├── api/ocrapp/         # OCR utilities for processing receipt images
├── fhrs/               # Food Hygiene Rating data
├── mycoffeeapp/        # Main Django project config (settings, URLs)
├── priceapp/           # Models & views for submitting/viewing price data
├── registration/       # Views & serializers for user auth
├── media/              # Folder for uploaded files (e.g., receipts)
├── static/             # Static files (admin panel, etc.)
├── requirements.txt    # Python dependencies
├── run_tests.py        # Runs the backend test suite
└── manage.py           # Django’s command-line interface

-------------------------------------------------------------------

✨ How to run locally (use these commands in the terminal)✨

1. Navigate to the backend folder:

cd backend

2. Create and activate a virtual environment (if not already):

python3 -m venv myenv
source myenv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Run migrations and start the server:


python manage.py migrate  
python manage.py runserver

-------------------------------------------------------------------

✨ Tests ✨

Run the backend tests with 
python manage.py test

Or for detailed coverage:
coverage run manage.py test
coverage html

-------------------------------------------------------------------

✨ Deployment Ready ✨

This backend is fully functional and can be deployed to a service like Heroku, Railway, or an Ubuntu server with Gunicorn + Nginx. Config files can be added as needed for production.

