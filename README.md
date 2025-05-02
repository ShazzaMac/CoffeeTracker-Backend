Project: Coffee Tracker
-------------------------------------------------------------------

Welcome to Cortado | The Coffee Tracker 
 — this is a full-stack web application to help users track, compare, and contribute data on coffee prices across cafes, powered by OCR technology and user submissions. It also makes use of open APIs to build a map and showcase user's favourite spots.
-------------------------------------------------------------------

✨ Architecture Overview ✨

 - Frontend: React (JavaScript)
 - Backend: Django REST Framework (Python)
 - Database: PostgreSQLCommunication: 
 - Axios (HTTP requests from frontend to backend)

 - Users interact via a modern React interface, while Django handles all backend logic and database operations.
-------------------------------------------------------------------

✨ Key Features ✨

 - Submit and view coffee prices

 - Upload receipts and extract data with OCR

 - Search and filter cafes by postcode, rating, and name

 - Visualize data with charts and leaderboards

 - Contact form with email delivery and admin storage

-------------------------------------------------------------------

✨ How It Works ✨

 - React handles the user interface

 - Axios sends data and fetches results via API endpoints

 - Django validates, processes, and stores the data

 - PostgreSQL (PGadmin4) keeps the backend data safe and queryable

-------------------------------------------------------------------

✨ Repository Structure ✨

my-webapp/
├── frontend/       # React framework (client)
├── backend/        # Django framework (API + database)

-------------------------------------------------------------------

✨ Project Structure ✨

.
├── README.md
├── backend
│   ├── accounts/               # Handles user profile logic and signals
│   ├── api/                    # Contains OCR-related logic
│   ├── fhrs/                   # FHRS API logic for coffee shop data
│   ├── manage.py               # Django management script
│   ├── media/                  # Uploaded receipts
│   ├── mycoffeeapp/            # Core Django app (settings, views, URLs)
│   ├── priceapp/               # Handles price submissions and features
│   ├── registration/           # Handles registration, login, and auth
│   ├── requirements.txt        # Python dependencies
│   ├── run_tests.py            # Test runner for backend
│   └── static/                 # Static files (e.g., admin CSS)
├── frontend
│   ├── public/                 # HTML template and favicon
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page-level React views
│   │   ├── services/           # API service files
│   │   └── utils/              # Utility functions
│   ├── jest.config.js          # Jest configuration for testing
│   ├── package.json            # Node.js dependencies
│   └── README.md               # Frontend usage instructions
├── project_structure.md        # This file (auto-generated)
└── start_project.sh            # Shell script for setup

-------------------------------------------------------------------


✨ Deployment ✨

The app is CI/CD-ready via GitHub Actions and can be deployed using any suitable deployment services or can be developed further.

