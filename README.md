# Django Movie App — Render Deployment

A Django application for displaying movies, viewing movie details, and adding movies with poster uploads. This project documents the journey from local development to deployment on Render, with WhiteNoise for static assets and Cloudinary for uploaded posters.

**Repository:** [JWulfran/django-movie-render](https://github.com/JWulfran/django-movie-render)

**Progress updated:** October 16, 2026.

**Live application:** [django-movie-render.onrender.com](https://django-movie-render.onrender.com)

> Deployment succeeded on October 16, 2026. Configuration examples must match the actual project settings. Production poster uploads and data persistence still need functional verification.

## Features covered

- Movie listing and movie detail pages.
- A form for adding movies, including a poster upload.
- Shared Django templates with page-specific CSS.
- Poster display using `{{ movie.poster.url }}` and a placeholder when no poster exists.
- Preparation for GitHub and Render deployment.
- Environment-based settings, static file serving, and external media storage.

## Technology stack

| Tool | Purpose |
| --- | --- |
| Python and Django | Application logic, forms, models, and templates |
| HTML, CSS, and Django templates | User interface |
| Pillow | Image handling for uploaded posters |
| Gunicorn | Production WSGI application server |
| WhiteNoise | Serving collected static assets |
| Cloudinary and django-cloudinary-storage | Storage and delivery of uploaded posters |
| python-dotenv | Loading local environment variables |
| dj-database-url and psycopg2-binary | PostgreSQL connection support |
| GitHub | Source code repository |
| Render | Application hosting and deployment |

Use `requirements.txt` as the source of truth for installed versions. The deployment migration command completed successfully. The log does not identify the database backend or establish persistent storage across redeployments.

## Important project files

The following paths were covered during development. This is a guide, not a verified inventory of the repository.

| Path | Purpose |
| --- | --- |
| `manage.py` | Runs Django management commands |
| `config/settings.py` | Application and deployment settings, if the settings package is named `config` |
| `config/wsgi.py` | WSGI entry point used successfully by Gunicorn |
| `MovieApp/views.py` | Movie application views |
| `base.html` | Shared template structure |
| `movie_detail.html` | Movie details and poster display |
| `static/css/movie_detail_style.css` | Movie detail page styling |
| `requirements.txt` | Python dependencies |
| `build.sh` | Render build script |
| `.env` | Local secrets and environment settings; excluded from Git |

## Run locally on Windows

Clone the repository and enter the project folder:

```powershell
git clone https://github.com/JWulfran/django-movie-render.git
cd django-movie-render
```

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the directory containing `manage.py`. Use variable names that match the names read by `settings.py`. For example:

```dotenv
SECRET_KEY=replace-with-a-local-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

The Cloudinary names above are examples; they work only when your settings read those exact names. Find the cloud name and API credentials in your Cloudinary account dashboard. Keep the API secret private.

If using `python-dotenv`, load the file before calling `os.getenv`:

```python
import os
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")
```

Here, `BASE_DIR` must already be defined in `settings.py`.

Apply existing migrations and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). To create an administrator account, run `python manage.py createsuperuser`.

## Environment-based Django settings

The configuration discussed uses environment variables for debugging and accepted hostnames:

```python
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
```

`DEBUG` becomes `True` when the supplied value is `true`, regardless of capitalization. `ALLOWED_HOSTS` converts a comma-separated string into a list and removes blank entries and surrounding spaces.

On Render, set `DEBUG=False` and use the actual service hostname in `ALLOWED_HOSTS`, without `https://` or a path.

## Static files and uploaded media

| File type | Examples | Deployment role |
| --- | --- | --- |
| Static files | CSS, JavaScript, application icons | Collected by Django and served with WhiteNoise |
| Media files | Movie posters uploaded through a form | Stored and delivered through Cloudinary |

`collectstatic` gathers application assets into `STATIC_ROOT`. WhiteNoise serves those assets in production. Uploaded posters need persistent external storage; they should not depend on the web service's temporary local filesystem.

In the movie detail template, the poster is displayed through the configured storage backend:

```django
{% if movie.poster %}
    <img src="{{ movie.poster.url }}" alt="Poster for {{ movie.title }}">
{% else %}
    <div class="poster-placeholder">No poster available</div>
{% endif %}
```

The local poster upload setup was reported as working before preparing the Render commands.

## Render build script

The build script covered so far is:

```bash
#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

Save it as `build.sh` beside `manage.py`, using LF line endings.

| Line | Purpose |
| --- | --- |
| `#!/usr/bin/env bash` | Selects Bash as the script interpreter |
| `set -o errexit` | Stops the script when a command fails |
| `pip install` | Installs project dependencies |
| `collectstatic --noinput` | Collects static assets without interactive prompts |
| `migrate --noinput` | Applies committed database migrations without interactive prompts |

With this order, a failure during static collection prevents the migration command from running.

## Render web service configuration

Connect the GitHub repository to a Render Python web service. The commands discussed are:

| Setting | Value |
| --- | --- |
| Repository | `JWulfran/django-movie-render` |
| Branch | `main` |
| Build command | `bash build.sh` |
| Start command | `python -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |

The start command assumes the package containing `wsgi.py` is named `config`. Replace `config` if the actual package has a different name.

Render supplies the `PORT` environment variable. You do not need to add it manually for this command. `$PORT` is expanded by the Render shell, and `0.0.0.0` lets the server accept incoming connections on the service network. Use `runserver` for local Windows development.

Set environment variables in the Render service settings:

| Variable | Production value or purpose |
| --- | --- |
| `SECRET_KEY` | A private production Django secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Actual Render service hostname; comma-separated if there are several |
| Cloudinary credentials | Cloud name, API key, and API secret using the names expected by your settings |
| `DATABASE_URL` | PostgreSQL connection URL, if the application settings use it |

Render environment variables are configured separately from your local `.env`. Merely adding `DATABASE_URL` does not configure Django: the `DATABASES` setting must read it. Confirm persistent database storage before relying on production records.

## GitHub preparation

Keep source code, templates, static source assets, migrations, `requirements.txt`, and `build.sh` in Git. Exclude local credentials and generated files. Suggested `.gitignore` entries:

```gitignore
env/
venv/
.venv/
__pycache__/
*.py[cod]
.env
.env.*
!.env.example
db.sqlite3
staticfiles/
media/
.vscode/
```

Track a `.env.example` containing placeholders if desired. If a secret was already committed, adding it to `.gitignore` does not remove it from Git history; replace the exposed credential.

After placing this README in the project root:

```powershell
git add README.md
git commit -m "Document movie app setup and Render deployment"
git push origin main
```

## Current deployment status

The latest supplied log confirms a successful deployment of commit `4852893dba9a8c8490e311831b3add00ea21cadf` from `main` on October 16, 2026.

| Stage | Result |
| --- | --- |
| Dependency installation | Successful |
| Static collection | 143 files copied, 429 post-processed |
| Database migrations | Completed; no migrations to apply |
| Render build | Successful |
| Gunicorn startup | Started and listening on `0.0.0.0:10000` |
| Service availability | Render reported the service live at 18:33:58 UTC |
| Home page `/` | HTTP 200 |
| Add movie form `/add/` | HTTP 200 |
| Requested CSS assets | HTTP 200 |

The previous `STATICFILES_STORAGE` error no longer occurs in this build. The log confirms the successful outcome but does not show the exact configuration change that resolved it.

Two additional messages appeared:

- `/favicon.ico` returned HTTP 404. The browser requested a tab icon that was not found. This does not block the movie pages; adding and referencing a favicon is a remaining polish task.
- Gunicorn logged that a response to a `HEAD` request included body bytes and dropped them. The request returned HTTP 200, and deployment continued successfully. Investigate the response handling if this message persists.

The log shows successful page requests, but no movie submission or poster upload. Those features and persistence after redeployment remain to be checked.

## Verification after a successful deployment

- Open the movie list and a movie detail page.
- Confirm CSS and other static assets load.
- Submit a movie with a poster and verify the image loads from Cloudinary.
- Confirm records and uploaded posters remain available after a redeployment.
- Check service logs for application errors.
- Confirm production uses `DEBUG=False` and the correct allowed hostname.

## Documentation

- [Render: Deploy a Django App](https://render.com/docs/deploy-django)
- [Render: Web Services and port binding](https://render.com/docs/web-services)
- [WhiteNoise: Using WhiteNoise with Django](https://whitenoise.readthedocs.io/en/stable/django.html)
- [Django: Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Cloudinary documentation](https://cloudinary.com/documentation)

## Author

Jean Gahoussou — Django development and deployment learning project.
