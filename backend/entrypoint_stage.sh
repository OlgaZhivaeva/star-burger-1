echo "Start makemigrations..."
python manage.py makemigrations --dry-run --check &&
echo "Start migrate..."
python manage.py migrate --noinput &&
while [ ! -f /star-burger/frontend/bundles-ready.flag ]; do
  echo "Waiting for frontend to be ready..."
  sleep 1
done
echo "Start collectstatic..."
python manage.py collectstatic --noinput &&
echo "Start server..."
gunicorn star_burger.wsgi:application --bind 0.0.0.0:8000 --workers 3
