FROM python:3.10
RUN apt-get update -y && apt-get upgrade -y
WORKDIR /test_2_marusich
COPY ./ ./
ENV PYTHONPATN=${PYTHONPATN}:${PWD}
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install