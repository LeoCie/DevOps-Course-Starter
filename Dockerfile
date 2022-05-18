FROM python:3.8-slim-buster as base 

RUN pip install poetry
WORKDIR /app/todo_app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY ./todo_app ./todo_app
EXPOSE 80

FROM base as production
CMD poetry run gunicorn -b "0.0.0.0:80" 'todo_app.app:create_app()'

FROM base as development
CMD poetry run flask run -h "0.0.0.0" -p 80