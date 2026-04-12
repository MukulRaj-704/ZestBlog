# Blog Project

A production-ready blog application built with Django. This repository provides a fully featured blogging platform with social interaction, user profiles, private messaging, and deployment-ready configuration.

## Summary

This project delivers a modern blog experience with:

- secure user authentication and profile management
- blog creation, editing, deletion, and publishing workflows
- search functionality for blog content
- likes and author following
- curated feed for followed authors
- private messaging with file sharing
- optional media hosting through Cloudinary
- asynchronous communication support with Django Channels

## Repository Layout

- `accounts/` — authentication, profile views, registration, login, logout, and profile editing
- `blog/` — blog posts, comments, likes, follow system, conversations, and chat features
- `config/` — global settings, URL routing, ASGI/WGSI application definitions
- `templates/` — HTML templates for the application and account pages
- `staticfiles/` — generated static assets ready for deployment
- `media/` — local file storage for uploads when Cloudinary is not enabled

## Requirements

- Python 3.11 or later
- Virtual environment support
- Dependencies are defined in `requirements.txt`

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install project dependencies:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create a superuser for administrative access:

```bash
python manage.py createsuperuser
```

5. Collect static assets:

```bash
python manage.py collectstatic
```

6. Run the application locally:

```bash
python manage.py runserver
```

7. Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Configuration

Use environment variables to control application settings:

- `SECRET_KEY` — Django secret key
- `DEBUG` — `True` or `False`
- `DATABASE_URL` — optional database connection string
- `REDIS_URL` — optional Redis connection for Channels
- `CLOUDINARY_URL` — optional Cloudinary media storage connection

## Deployment

A `Procfile` is provided for deployment environments that support Daphne.

```bash
web: daphne -p $PORT config.asgi:application
```

Deployment behavior:

- Use Cloudinary when `CLOUDINARY_URL` is configured
- Use Redis for channel layers when `REDIS_URL` is configured
- Default to local `media/` storage and in-memory channels when not configured

## Common Commands

- `python manage.py migrate`
- `python manage.py runserver`
- `python manage.py createsuperuser`
- `python manage.py collectstatic`

## Additional Details

- Custom user model: `accounts.User`
- Static assets are served using WhiteNoise in production
- User profiles are created automatically via Django signals

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a descriptive branch name
3. Implement your changes
4. Submit a pull request with a concise summary of your work

## License

This project does not include a license by default. Add a license file if you intend to publish or share the code publicly.
