@echo off

REM Gaybeck Starkids SMS - Web App Setup Script for Windows

echo Setting up Django Web App...

REM Create Python virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file
if not exist .env (
    echo SECRET_KEY=your-secret-key-change-in-production > .env
    echo DEBUG=True >> .env
    echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env
)

REM Run migrations
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

REM Collect static files
python manage.py collectstatic --noinput

echo.
echo Setup complete! Start the server with: python manage.py runserver
pause
