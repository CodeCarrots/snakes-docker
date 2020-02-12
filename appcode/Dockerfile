FROM python:3.8-alpine

RUN \
    addgroup app && \
    adduser -D -H -h /srv/appenv -G app app && \
    mkdir -p /srv/appenv && \
    chown app:app /srv/appenv

ENV \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

## --- 8< ----
## prepare the chroot jail here...

RUN apk add bash procps

RUN \
    mkdir -p /jail/zygote && \
    cd /jail/zygote && \
    mkdir -p \
            bin \
            lib \
            usr/include \
            usr/lib \
        && \
    cp -L /bin/bash ./bin/ && \
    cp -L /usr/local/bin/python3.8 ./bin/python && \
    cd /lib && \
    cp -L \
            ld-musl-x86_64.so.1 \
            libc.musl-x86_64.so.1 \
            libz.so.1 \
        /jail/zygote/lib && \
    cp -RL /usr/local/lib/libpython3.8.so.1.0 \
        /usr/local/lib/python3.8 \
        /jail/zygote/usr/lib/

#    cp -R /usr/local/include/python3.8 /jail/zygote/usr/include/ && \

## --- 8< ----

WORKDIR /srv/appenv

COPY snakes/requirements.txt /srv/appenv/

RUN \
    pip install --upgrade pip && \
    pip install --no-cache-dir --requirement requirements.txt

COPY snakes /srv/appenv/snakes

RUN \
    cd /srv/appenv/snakes && \
    pip install .

COPY snakes/django_snakes /srv/appenv/app

RUN python -m compileall app

RUN mkdir -p /srv/appenv/app/static

## --- 8< ----

WORKDIR /srv/appenv/app

COPY docker-entrypoint.sh /_run

RUN /_run django-manage collectstatic -c --noinput

USER app

ENTRYPOINT ["/_run"]

CMD ["shell"]
