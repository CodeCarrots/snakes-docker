#!/bin/bash

# NOTE: this script assumes the CWD is /srv/appenv/app

set -e

source /srv/appenv/py3env/bin/activate

case "$1" in
    django-manage)
        shift
        exec python manage.py "$@"
        ;;

    django-run|django-devrun)
        : ${APP_PORT:=8000}
        : ${APP_WSGI:=django_snakes}

        if [ "$1" = 'django-devrun' ]; then
            DO_RELOAD='--reload'
        fi

        exec gunicorn "${APP_WSGI}.wsgi" $DO_RELOAD --access-logfile - \
             -w 2 -b :$APP_PORT
        ;;

    manage)
        shift
        exec snakes-manage "$@"
        ;;

    snakes-run)
        if [ "$UID" -ne '0' ]; then
            echo "snakes server requires UID 0"
            exit 1
        fi

        shift
        exec snakes-server "$@"
        ;;
esac

exec "$@"
