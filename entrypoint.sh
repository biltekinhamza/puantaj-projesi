#!/bin/sh
set -e

python manage.py makemigrations personel ayarlar puantaj ek_kazanc kesintiler --noinput
python manage.py migrate --noinput
python manage.py seed_defaults
python manage.py ensure_superuser

if [ "$AUTO_IMPORT_PERSONEL" = "1" ]; then
  python manage.py import_personel_json --path data/personeller.json || true
fi

python manage.py collectstatic --noinput || true

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
