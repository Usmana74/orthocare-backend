release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn orthocare_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
