# Django Movie App

A small Django project for learning deployment on Render.

## Features

- Browse saved movies
- Add movies with optional posters
- View individual movie details

## Run locally

1. Create a virtual environment:

   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Generate a secret key and put it in `.env`:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Apply migrations and start the server:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/.

## Data and uploads

The local SQLite database and uploaded posters are excluded from Git.
A new installation starts with an empty database.