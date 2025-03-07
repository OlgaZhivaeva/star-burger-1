echo "Start makemigrations..."
python manage.py makemigrations --dry-run --check &&
echo "Start migrate..."
python manage.py migrate --noinput &&
while true; do
  FRONTEND_STATUS=$(docker inspect -f '{{.State.Status}}' frontend)
  if [ "$FRONTEND_STATUS" = "exited" ]; then
    break
  fi
  echo "Waiting for frontend to be ready..."
  sleep 1
done
echo "Start collectstatic..."
python manage.py collectstatic --noinput &&
echo "Start server..."
gunicorn star_burger.wsgi:application --bind 0.0.0.0:8000 --workers 3
