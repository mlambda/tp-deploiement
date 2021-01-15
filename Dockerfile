FROM python:3.8.7-slim-buster as builder

WORKDIR /app

RUN apt update \
    && apt install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    gfortran \
    libgl1-mesa-glx \
    libopenblas-dev \
    liblapack-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY poetry.lock ./

COPY pyproject.toml ./

RUN /root/.poetry/bin/poetry install --no-dev

COPY . .

RUN /root/.poetry/bin/poetry install --no-dev

CMD ["/root/.poetry/bin/poetry", "run", "landscapred"]
