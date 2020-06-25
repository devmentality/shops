FROM python:3.8-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONFAULTHANDLER=true
ENV PYTHONUNBUFFERED=true

WORKDIR /code

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        gcc \
        libsasl2-dev \
        libldap2-dev \
        libssl-dev \
        graphviz \
        libgraphviz-dev \
        libpq-dev \
        make \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock Makefile /code/

RUN pip install --no-compile --upgrade pip
RUN pip install --no-compile poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi
RUN pip uninstall --yes poetry


COPY ./shops /code/shops

EXPOSE 8000
ENTRYPOINT [""]
CMD ["make", "up"]
