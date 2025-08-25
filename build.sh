#!/usr/bin/env bash
# exit on error
set -o errexit

# Debug: Print environment variables
echo "Checking environment variables..."
echo "SECRET_KEY: ${SECRET_KEY:0:10}..."  # Only show first 10 chars for security
echo "DATABASE_URL: ${DATABASE_URL:0:20}..."  # Only show first 20 chars
echo "DEBUG: $DEBUG"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"

# Ensure SECRET_KEY is set
if [ -z "$SECRET_KEY" ]; then
    echo "Warning: SECRET_KEY not set, using default"
    export SECRET_KEY="django-insecure-change-this-in-production-please-change-in-production-environment"
fi

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Check if DATABASE_URL is set and valid
if [ -n "$DATABASE_URL" ] && [[ "$DATABASE_URL" == postgresql://* ]]; then
    echo "PostgreSQL database URL detected, running migrations..."
    python manage.py migrate
    python manage.py setup_cms
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@givegrip.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
else
    echo "No valid DATABASE_URL found, skipping database operations"
    echo "This is normal for the first deployment before database linking"
fi
