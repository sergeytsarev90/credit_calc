FROM registry.ae-rus.net/mirror/python:3.9-slim
WORKDIR /app
COPY . /app

ENV PIPENV_PYPI_MIRROR="https://nexus.ae-rus.net/repository/pypi-group/simple/" \
    PIPENV_VENV_IN_PROJECT="true"

RUN pip install pipenv
RUN apt-get update
RUN apt-get -qq -y install zip curl python3-dev

ENV PYTHONPATH "${PYTHONPATH}:${PWD}"
RUN pipenv sync

EXPOSE 80

CMD ["pipenv", "run", "python", "main.py"]
