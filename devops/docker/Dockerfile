FROM python:3.11.3-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
              gcc=4:* \
              libc6-dev=2.* \
              binutils=2.* \
              gettext=0.* \
              nginx=1.* \
              make=4.* \
              curl=7.* \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/install-poetry.py | python - \
    && poetry install --no-dev --no-interaction --no-ansi \
    && apt-get remove --purge -y gcc binutils \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf "$POETRY_CACHE_DIR"

# ---

FROM base as production

COPY devops/docker/server .
COPY devops/docker/nginx/* /etc/nginx
COPY ./src ./src

RUN export DJANGO_ENV=build \
    && python src/manage.py collectstatic --noinput --verbosity 0 \
    && python src/manage.py compilemessages \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --no-log-init -g app app \
    && chmod -R 755 /app \
    && mkdir /var/run/app \
    && mkdir /var/run/nginx \
    && chown app:app /var/run/nginx \
    && chown app:app /var/run/app \
    && chown app:app /var/log/nginx \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log


ENV DJANGO_ENV=production

USER app

CMD ["make", "server"]

# ---

FROM base as test

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN export DJANGO_ENV=build \
    && python src/manage.py compilemessages

