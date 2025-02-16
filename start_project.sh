#!/bin/bash

# Navigate to backend and activate virtual environment
cd backend
source myenv/bin/activate  # Activate the virtual environment

# Start Django server
python3 manage.py runserver &  # Run in background

# Navigate to frontend and start React app
cd ../frontend
npm start  # Start the React frontend

# Keep script running
wait
