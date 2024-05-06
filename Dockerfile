FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements.txt

EXPOSE 5000

USER nobody

ENTRYPOINT ["/usr/bin/env", "uwsgi", "--http", ":5000", "--ini", "uwsgi.ini"]
CMD ["--processes", "2", "--threads", "2"]
