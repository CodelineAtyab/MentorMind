@echo off
echo Starting MentorMind Attendance App Setup...

REM 1. Create attendance directory in current location
echo Creating attendance database directory...
mkdir mentor-mind-attendance-db
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not create directory, it may already exist.
)

REM 2. Get the absolute path of the script directory
SET "SCRIPT_DIR=%~dp0"
REM Calculate the absolute path of the attendance database directory
SET "DB_DIR=%SCRIPT_DIR%mentor-mind-attendance-db"
echo Database directory path: %DB_DIR%

REM 3. Run docker with the attendance database directory as source for bind mount
echo Starting Docker container...
docker run --name mentor-mind-attendance-ease -d -p 8889:8888 -v "%DB_DIR%:/app/data" syedatyab/mm-basic-attendance-app:0.0.1

REM Wait a moment for Docker to initialize
echo Waiting for container to initialize...
timeout /t 5 /nobreak > nul

REM 4. Open default browser to the application
echo Opening application in browser...
start http://localhost:8889

echo Setup complete! Application should be running at http://localhost:8889