FROM python:3.10
RUN apt-get update -y && apt-get upgrade -y
WORKDIR /app
COPY ./poetry.lock ./
COPY ./pyproject.toml ./
COPY ./main_app ./
ENV PYTHONPATN=${PYTHONPATN}:${PWD}
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install