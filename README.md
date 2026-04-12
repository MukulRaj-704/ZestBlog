# Blog Project

A Django blog platform with social features, user profiles, messaging, and cloud-friendly media storage.

## Key Features

- User authentication: register, login, logout
- Custom user profile with avatar and bio
- Create, edit, delete, and publish blog posts
- Search blogs by title or content
- Like/unlike blog posts
- Follow/unfollow other users
- Following feed to view posts from followed accounts
- Blog sharing via private conversations
- Direct messaging inbox with file upload support
- Cloudinary media storage support for production
- WebSocket support via Django Channels and Daphne

## Project Structure

- `accounts/` — custom user model, registration, login, profiles, edit profile, password change
- `blog/` — blog posts, comments, likes, follow system, conversations, file sharing
- `config/` — Django settings, ASGI/WGSI config, URL routing
- `templates/` — HTML templates for the main app and accounts
- `staticfiles/` — collected static assets
- `media/` — uploaded media files when not using Cloudinary

## Requirements

This project uses Python and Django, plus the dependencies listed in `requirements.txt`.

Install dependencies:

```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

The app supports these optional environment variables:

- `SECRET_KEY` — Django secret key
- `DEBUG` — set to `True` or `False` (default is `True`)
- `DATABASE_URL` — optional database URL for production
- `REDIS_URL` — optional Redis URL for Channels layer
- `CLOUDINARY_URL` — optional Cloudinary connection string for media storage

## Local Setup

1. Activate the virtual environment.
2. Install requirements.
3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Collect static files (optional for deployment):

```bash
python manage.py collectstatic
```

6. Start the development server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Deployment Notes

This project is configured for deployment with Daphne and Cloudinary support.

The provided `Procfile` uses:

```bash
web: daphne -p $PORT config.asgi:application
```

If `CLOUDINARY_URL` is set, media uploads are stored in Cloudinary. Otherwise, media files are stored locally in `media/`.

If `REDIS_URL` is set, Django Channels uses Redis for channel layers; otherwise it falls back to the in-memory channel layer.

## Useful Commands

- `python manage.py migrate`
- `python manage.py runserver`
- `python manage.py createsuperuser`
- `python manage.py collectstatic`

## Notes

- `AUTH_USER_MODEL` is set to `accounts.User`
- Static files use WhiteNoise in production
- The project includes both `channels` and `daphne` for asynchronous support
- Custom user profiles are created automatically via Django signals
