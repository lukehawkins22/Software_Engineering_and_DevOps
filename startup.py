import os

# Run collectstatic command
os.system("python manage.py collectstatic")

# Run runserver command
os.system("python manage.py runserver 0.0.0.0:8000 --noreload")

