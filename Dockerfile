FROM python:3.8-slim-buster as base 

RUN pip install poetry
COPY poetry.lock pyproject.toml /app/todo_app/
WORKDIR /app/todo_app
RUN poetry install
COPY . .
EXPOSE 80

FROM base as production
CMD poetry run gunicorn -b "0.0.0.0:80" 'todo_app.app:create_app()'

FROM base as development
CMD poetry run flask run -h "0.0.0.0" -p 80