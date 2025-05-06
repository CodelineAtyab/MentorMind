@echo off
echo Starting MentorMind Attendance App Setup...

REM 1. Create attendance directory in current location
echo Creating attendance database directory...
mkdir mentor-mind-attendance-db
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not create directory, it may already exist.
)

REM 2. Get the absolute path of the parent directory of the script
SET "SCRIPT_DIR=%~dp0"
REM Get parent directory (one level up from script location)
for %%I in ("%SCRIPT_DIR%..") do SET "PARENT_DIR=%%~fI"
echo Parent directory path: %PARENT_DIR%

REM 3. Run docker with the parent directory as source for bind mount
echo Starting Docker container...
docker run --name mentor-mind-attendance-ease -d -p 8889:8888 -v "%PARENT_DIR%:/app/data" syedatyab/mm-basic-attendance-app:0.0.1

REM Wait a moment for Docker to initialize
echo Waiting for container to initialize...
timeout /t 5 /nobreak > nul

REM 4. Open default browser to the application
echo Opening application in browser...
start http://localhost:8889

echo Setup complete! Application should be running at http://localhost:8889