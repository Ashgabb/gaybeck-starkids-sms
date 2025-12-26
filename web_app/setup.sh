#!/bin/bash

# Gaybeck Starkids SMS - Web App Setup Script

echo "Setting up Django Web App..."

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "SECRET_KEY=your-secret-key-change-in-production" > .env
    echo "DEBUG=True" >> .env
    echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
fi

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

echo "Setup complete! Start the server with: python manage.py runserver"
