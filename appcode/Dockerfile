FROM python:3.8-buster

RUN useradd -M -U -d /srv/appenv app && \
    mkdir -p /srv/appenv && \
    chown app:app /srv/appenv

ENV \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

## --- 8< ----
## prepare the chroot jail here...

RUN mkdir -p /jail/zygote && \
    cd /jail/zygote && \
    mkdir -p bin \
             lib64 \
             lib/x86_64-linux-gnu \
             usr/include \
             usr/lib && \
    cp -L /bin/bash ./bin/ && \
    cp -L /usr/local/bin/python3.8 ./bin/python && \
    cd /lib/x86_64-linux-gnu && \
    cp -L libc.so.6 \
       libcrypt.so.1 \
       libdl.so.2 \
       libexpat.so.1 \
       libm.so.6 \
       libpthread.so.0 \
       librt.so.1 \
       libutil.so.1 \
       libz.so.1 \
       /jail/zygote/lib/x86_64-linux-gnu && \
    cp -L /lib64/ld-linux-x86-64.so.2 /jail/zygote/lib64 && \
    cp -RL /usr/local/lib/libpython3.8.so.1.0 \
        /usr/local/lib/python3.8 \
        /jail/zygote/usr/lib/

#    cp -R /usr/local/include/python3.8 /jail/zygote/usr/include/ && \

## --- 8< ----

RUN python3.8 -m venv /srv/appenv/py3env

WORKDIR /srv/appenv

COPY snakes/requirements.txt /srv/appenv/

RUN . /srv/appenv/py3env/bin/activate ; \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY snakes /srv/appenv/snakes

RUN . /srv/appenv/py3env/bin/activate ; \
    cd /srv/appenv/snakes && pip install .

COPY snakes/django_snakes /srv/appenv/app

RUN . /srv/appenv/py3env/bin/activate ; \
    python -m compileall app

RUN mkdir -p /srv/appenv/app/static


## --- 8< ----

WORKDIR /srv/appenv/app

COPY docker-entrypoint.sh /_run

RUN /_run django-manage collectstatic -c --noinput

USER app

ENTRYPOINT ["/_run"]

CMD ["shell"]
