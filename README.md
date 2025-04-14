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

✨ Deployment ✨

The app is CI/CD-ready via GitHub Actions and can be deployed using any suitable deployment services or can be developed further.

