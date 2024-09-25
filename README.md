# API Library
A simple FastAPI project using SQLAlchemy 2.0 with user JWT authentication. Provides an API for crud operations on book and author objects

## Features
- PostgreSQL
- Pydantic 2
- SQLAlchemy 2.0
- running with docker compose
- Alembic for datatbase migration
- user authentication with JWT

## Installation
Clone this repo to your local machine:
```sh
git clone https://github.com/GrigoriyKuzevanov/fastapi-sqlalchemy-library.git
```
Get into project work directory and create a `.env` file:
```sh
cd fastapi-sqlalchemy-library/
touch .env
```
Inside of `.env` file create settings variables.

- For app info:
```
# App info settings - Optional variables
APP_NAME="Your name for the app"  # Default: "FastAPI project"
APP_DESCRIPTION="Your app description"
APP_VERSION="Your app version"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
CONTACT_URL="Your url"
```
- For create admin user:
```
ADMIN_EMAIL="Your admin email"
ADMIN_PASSWORD="Your admin password"
```
- For the main database. You can use docker db or create your own db:
```
# main Postrgres db
DB_USER="Your postgres user name"
DB_PASSWORD="Your password for user"
DB_HOST=db-"db-main" # your can change it for using with your database 
DB_PORT=5432  # your can change it for using with your database
DB_NAME="Your postgres db name"
ECHO_SQL=False  # you can change it to True and SQLAlchemy will log all statements to console by default
```
- For testing db. You can use docker db or create your own db: 
```
# test Postrgres db
TEST_DB_USER="Your testing postgres user name"
TEST_DB_PASSWORD="Your password for user"
TEST_DB_HOST=db-test  # your can change it for using with your database
TEST_DB_PORT=5432  # your can change it for using with your database
TEST_DB_NAME="Your testing postgres db name"
```
- For users authentication. You should generate your own secret key by `openssl rand -hex 32` command:
```
# Oauth2 settings
SECRET_KEY="Your secret key"  # make sure that secret key value not in public
ALGORITHM=HS256  # algorithm for hash user's passwords to keep in db, you can change it
ACCESS_TOKEN_EXPIRE_MINUTES=30  # you can change access token lifetime
```
- CORS settings:
```
#CORS
# write down your origins or set it to '*' for all origins
# EXAMPLE: CORS_ORIGINS=www.example.com, www.hello.com, www.github.com
CORS_ORIGINS=*
```

## Usage (with docker compose)
After setting project variables you can start docker compose:
```sh
docker compose up
```
You can create admin user. Get into app docker containder:
```sh
docker exec -it <container-id> bash
python3 -m app.scripts.create_first_admin
```