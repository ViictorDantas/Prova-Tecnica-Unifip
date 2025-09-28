#!/bin/sh
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -q; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"