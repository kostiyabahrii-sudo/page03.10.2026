#!/usr/bin/env bash
# Команда збірки на Render.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
