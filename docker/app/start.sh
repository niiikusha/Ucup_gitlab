#!/bin/bash

NAME="LAMA_ucup app"
echo "Starting $NAME as `whoami`"

PROC_NUM="$(getconf _NPROCESSORS_ONLN)"
THREADS=$(($PROC_NUM * 2))

case ${DEV_SERVER} in
  true | 1)
    echo "Check migrations"
    python3 manage.py check
    python3 manage.py makemigrations --noinput
    ;;
  *)
    ;;
esac

echo "Migrating..."
python3 manage.py check
python3 manage.py migrate --noinput

echo "Translation..."
python3 manage.py makemessages -l en
python3 manage.py makemessages -l ru

echo "Statics..."
python3 manage.py collectstatic --noinput
case ${DEV_SERVER} in
  true | 1)
    echo "======================================="
    echo "| Starting django development server |"
    echo "======================================="
    exec python3 manage.py runserver --configuration=Docker 0.0.0.0:8001
    ;;
  *)
    echo "========================="
    echo "| Starting uWSGI server |"
    echo "========================="
    exec uwsgi \
      --http :8001 \
      --module app.wsgi \
      --env DJANGO_SETTINGS_MODULE=app.settings \
      --chdir=/app \
      --workers=$THREADS \
      --max-requests=1000 \
      --master \
      --enable-threads \
      -L
    ;;
esac
