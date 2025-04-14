#---------------------------------------------------------------
# This script sets up both the frontend and backend of the app without having to do it separately
# To use type in ./start_project.sh in the terminal
#---------------------------------------------------------------


# Navigate to backend and activate virtual environment
cd backend
source myenv/bin/activate  # Activates the virtual environment

# Start Django server
python3 manage.py runserver &  # Run in background

# Navigate to frontend and start React app
cd ../frontend
npm start  # Start the React frontend

# Keep script running
wait
