#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Setup CMS data if it doesn't exist
python manage.py setup_cms

# Create superuser if it doesn't exist (will be skipped if already exists)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@givegrip.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
