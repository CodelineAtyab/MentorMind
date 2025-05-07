#!/bin/bash
echo "Starting MentorMind Attendance App Setup..."

# 1. Create attendance directory in current location
echo "Creating attendance database directory..."
mkdir -p mentor-mind-attendance-db
if [ $? -ne 0 ]; then
    echo "Warning: Could not create directory, it may already exist."
fi

# 2. Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Calculate the absolute path of the attendance database directory
DB_DIR="${SCRIPT_DIR}/mentor-mind-attendance-db"
echo "Database directory path: $DB_DIR"

# 3. Run docker with the attendance database directory as source for bind mount
echo "Starting Docker container..."
docker run --name mentor-mind-attendance-ease -d -p 8889:8888 -v "$DB_DIR:/app/data" syedatyab/mm-basic-attendance-app:0.0.1

# Wait a moment for Docker to initialize
echo "Waiting for container to initialize..."
sleep 5

# 4. Open default browser to the application
echo "Opening application in browser..."
# Try different methods to open browser based on OS
if command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:8889
elif command -v open &> /dev/null; then
    # macOS
    open http://localhost:8889
else
    echo "Could not open browser automatically. Please navigate to http://localhost:8889"
fi

echo "Setup complete! Application should be running at http://localhost:8889"
