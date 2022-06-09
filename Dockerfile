FROM python:3.8-slim-buster as base 

RUN pip install poetry
WORKDIR /app/todo_app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY ./todo_app ./todo_app
EXPOSE 80

FROM base as production
CMD poetry run gunicorn -b "0.0.0.0:${PORT:-80}" "todo_app.app:create_app()"

FROM base as development
CMD poetry run flask run -h "0.0.0.0" -p 80

FROM base as test
# Copy test files
COPY ./todo_app_tests ./tests
COPY ./todo_app_tests_e2e ./tests_e2e

# Install test dependencies
RUN poetry install
ENV GECKODRIVER_VER v0.30.0
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

ENTRYPOINT [ "poetry", "run", "pytest" ]