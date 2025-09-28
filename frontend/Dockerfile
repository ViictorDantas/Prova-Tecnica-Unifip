FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /frontend

COPY front.env .
COPY . .
COPY scripts /scripts
RUN chmod +x /scripts/migrate.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY requirements.txt .
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/venv/bin:$PATH"

EXPOSE 8001

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001" ]
