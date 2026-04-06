# Make sure this matches runtime.txt
FROM python:3.13

LABEL org.opencontainers.image.source=https://github.com/noisebridge/library-org
LABEL org.opencontainers.image.description="Organizational system for a library"
LABEL org.opencontainers.image.licenses=MIT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . /app/
RUN uv sync --frozen --no-dev

EXPOSE 5000

USER nobody

ENTRYPOINT ["/app/.venv/bin/uwsgi", "--http", ":5000", "--ini", "uwsgi.ini"]
CMD ["--processes", "2", "--threads", "2"]
