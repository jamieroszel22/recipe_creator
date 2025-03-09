@echo off
echo Recipe Creator - Deployment Script
echo ==================================

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker is not installed. Please install Docker first.
    echo Visit: https://docs.docker.com/get-docker/
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    echo Visit: https://docs.docker.com/compose/install/
    exit /b 1
)

REM Build and start the containers
echo Building and starting containers...
docker-compose up -d --build

REM Wait for the application to start
echo Waiting for the application to start...
timeout /t 10 /nobreak > nul

REM Check if the application is running
curl -s http://localhost:8000/health > nul
if %ERRORLEVEL% EQU 0 (
    echo Application is running!
    echo You can access it at: http://localhost:8000
    
    REM Get the IP address for sharing on the same network
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
        set IP=%%a
        goto :found_ip
    )
    :found_ip
    if defined IP (
        echo Share on your network at: http:%IP:~1%:8000
    )
    
    echo.
    echo To view logs: docker-compose logs -f
    echo To stop: docker-compose down
) else (
    echo Application failed to start. Check logs with: docker-compose logs -f
) 