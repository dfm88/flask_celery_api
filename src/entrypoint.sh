#!/bin/sh
set -e
MIGRATIONS_DIR="./migrations"
if [ -d "$MIGRATIONS_DIR" ]; then
  echo "migrations exists..."
else
  echo "init db..."
    flask db init 
fi
flask db migrate
flask db upgrade
python run.py