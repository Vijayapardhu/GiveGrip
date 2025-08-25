#!/usr/bin/env python
"""
Setup script for GiveGrip database and CMS
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'givegrip.settings')
django.setup()

from django.core.management import execute_from_command_line

def setup_database():
    """Set up the database and CMS data."""
    print("Setting up GiveGrip database...")
    
    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Set up CMS data
    print("Setting up CMS data...")
    execute_from_command_line(['manage.py', 'setup_cms'])
    
    print("Database setup completed!")

if __name__ == '__main__':
    setup_database()
