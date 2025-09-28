FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY api /api
COPY scripts /scripts

WORKDIR /api

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /api/requirements.txt && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

EXPOSE 8000

CMD [ "commands.sh" ]