# Weather App

This is a simple REST API for a weather app. It is implemented with Django/Django Rest
Framework (DRF) with a PostgreSQL database. A configuration to deploy using Docker Compose
is included along with a Postman collection.

## Functionality

The minimum requirements for this API were to be able to add measurements and be able to
update them, while enforcing validation and constraints in the fields that can be updated.
Additionally, the API should be able to list the measurements and have the ability to filter
by station and date parameters.

These functionalities are implemented by the current implementation. Additionally, a user
hierarchy is created in order to implement a permissions scheme. There are three kinds of users:

- Admin users: Admins have permission to interact with all endpoints.
- Viewers: Simple users who have only view access.
- Service station users: These users have the same permissions as viewers, but additionally they
  are associated with a service station and can also POST measurements, but only for the station
  that is associated with them.

Simple users can be created by registering using the `POST http://localhost:8000/api/v1/users/`
endpoint. The other types of users can be created by running the command:

`python manage.py create_user`.

If the API is running in a container, first we must run the container interactively:

`docker exec -it <container_id> /bin/bash`

and then we can run the `create_user` command.

For authenticating users, JWT token authentication is used.

There are also endpoints for stations management. Each station must be associated with a service
station user.

For testing all functionalities an admin user is required. In the last section of this README,
credentials are provided for all types of users.

## Deploying with Docker Compose

The easiest way to deploy the API is by using the `docker-compose.yml` in the root directory.

The `docker-compose.yml` can be run directly. If the image for the API is not built, it will
be built by default. To deploy the `docker-compose.yml`, run (in the root directory):

`docker compose up -d`

In total, 4 containers will be created:

- The container with the PostgreSQL database (using port `5432`).
- The container with the Weather REST API, which will be available at http://localhost:8000/.
- One container which runs the Django migrations and populates the db with an initial dataset.
- One container which will run the tests. The API container deploys only if the tests run successfully.

These last two containers will exit upon completing their execution.

Optionally, the image for the API can be built independently using the individual Dockerfile.
To build it, run the command (in the root directory):

`docker build -t <image-tag> .`

The image tag used in the `docker-compose.yml` is `weather_app_be`. If the dockerfile is built
with another image tag, this tag can be set in the `docker-compose.yml` to avoid rebuilding the
image upon `docker compose` execution.

The API spec can be viewed in the `http://localhost:8000/api/v1/schema/swagger-ui/` or
`http://localhost:8000/api/v1/schema/redoc/` urls and can be downloaded with the
`http://localhost:8000/api/v1/schema/` url.

## Project Structure

The implementation is located in the `src/weather_app` directory. This includes:

- `config`: The basic Django project configuration directory.
- `common`: Some common utilities.
- `auth`: Django app which implements user authentication.
- `users`: Django app which implements user management.
- `stations`: Django app which implements weather stations management.
- `measurements`: Django app which implements weather measurements management.
- `pytest.ini` and `conftest.py`: Configuration files for testing with pytest.
- `manage.py`: The entry point for the api.
- `tests`: Contains the tests for the Weather app functionality.

## Deploy locally - Backend

The API is implemented with **Python 3.12**. All dependencies are included in the
`requirements.txt` file within the root directory. In order to run locally:

- Create a Python 3.12 virtualenv.
- Activate the environment.
- Run `pip install -r requirements.txt` in the root directory.
- Add `./src` directory to PYTHONPATH:
  `export PYTHONPATH="${PYTHONPATH}:/<path-to-add>"`.
- Deploy the container with the Postgres database: `docker compose up -d postgres_db`
- Update the local settings for the database at:
  `src/weather_app/config/settings/local.py`.
- `cd` to `src/weather_app`
- Create the private key for JWT authentication: Run `openssl genrsa -out rsa-private-key.pem 2048`
- Create the public key: Run `openssl rsa -in rsa-private-key.pem -pubout -outform PEM -out rsa-public-key.pem`.
  Note that if different names are used for the output files, they need to be updated in
  the environment variables. The variables that need to be set can be found in the .env file.
- Run `python manage.py migrate` to create the database tables.
- Run `python manage.py loaddata ./tests/data/initial_data.json` to add an initial
  dataset in the db (optional).
- Run `python manage.py runserver 0.0.0.0:8000` to start the local server.

It is possible to use the deployed settings or the local settings by setting
the `DJANGO_SETTINGS_MODULE`environment variable.

## Testing

The tests are implemented using the `pytest` and `pytest-django` frameworks. They can be
run with the following command (run in `src/weather_app`):

```pytest```

The configuration of the test suite can be found in the `conftest.py` and `pytest.ini`
files.

Note that the above path needs to be added to PYTHONPATH and the database container to be
running in order for the tests to succeed. Extra care needs to be taken to ensure that the
Django settings module that the pytest.ini points to is the correct one in order to connect
with the database.

### Initial data

The initial dataset can be found in `src/weather_app/tests/data/initial_data.json`.
This is a Django dump of the db at some point in development and is also used
by the test suite.

For simplifying testing, the credentials of the admin user are:
`{"email": "admin@weatherapp.com", "password": "123admin"}`

Credentials for service station user:
`{"email": "station0@weatherapp.com", "password": "123station0"}`

And finally, credentials for viewers:
`{"email": "user@test.com", "password": "123user"}`

Since this is a technical skills assignment in the context of an interview process,
exposing them in a README is done for the sole reason of simplifying the evaluation.
