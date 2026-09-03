<div align="center">

<h1>
    Cinelog
</h1>

<h3>
    Cinelog is an open-source app for discovering movies and TV shows and building your perfect watchlist.
</h3>

![release](https://img.shields.io/badge/version-v0.1-blue)

</div>

<p align="center">
    <a href="#technologies">Technologies</a> •
    <a href="#features">Features</a> •
    <a href="#requirements">Requirements</a> •
    <a href="#setup">Setup</a> •
    <a href="#environment-variables">Environment variables</a> •
    <a href="#modules">Modules</a> •
    <a href="#how-to-contribute">How to contribute</a> •
    <a href="#license">License</a> •
    <a href="#contact">Contact</a> 
</p>

## Technologies
- Python 3.14
- Django 6.1
- PostgreSQL 18
- Docker

## Features
- [x] User authentication
- [ ] Movie and TV show catalog
- [ ] Catalog search
- [ ] Custom public and private watchlists
- [ ] Social profiles

## Requirements
- Docker
- Docker Compose
- Git

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cinelog
   ```
2. Create a `.env` file in the project root and add the variables listed in `.env.example`.

3. Build and start the containers:
    ```bash
    docker compose up --build -d
    ```

4. Run Django database migrations:
    ```bash
    docker compose exec web python manage.py migrate
    ```

5. Open the application at: http://localhost:8000

## Environment variables

| Variable | Description |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key |
| `DATABASE_NAME` | PostgreSQL database name |
| `DATABASE_USER` | PostgreSQL user |
| `DATABASE_PASSWORD` | PostgreSQL password |
| `DATABASE_HOST` | PostgreSQL host (`db` when using Docker Compose) |
| `DATABASE_PORT` | PostgreSQL port (`5432` by default) |
| `EMAIL_HOST` | SMTP server |
| `EMAIL_PORT` | SMTP server port |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `MOVIE_API_TOKEN` | TMDB API token |

## Modules
- `main`: Django project configuration
- `accounts`: Authentication and account management
- `pages`: Generic application pages
- `catalog`: TMDB movie and TV show catalog and search
- `users`: User profiles and social features

## How to contribute
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a pull request.

## License
Cinelog is licensed under the [MIT License](LICENSE).

## Contact
<img align="left" src="https://avatars.githubusercontent.com/ArthurCostaBR?size=100">

    - Email: arthurdacosta.br@gmail.com
    - LinkedIn: linkedin.com/in/arthurcostabr/
    - Made by Arthur Costa