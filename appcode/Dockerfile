FROM debian:jessie

RUN apt-get update && \
    apt-get install -o APT::Install-Recommends=false \
                    -o APT::Install-Suggests=false -y \
                    python3.4 python3.4-venv && \
    apt-get clean

RUN useradd -M -U -d /srv/appenv app && \
    mkdir -p /srv/appenv && \
    chown app:app /srv/appenv

ENV PYTHON_PIP_VERSION=8.1.1 \
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
    cp /usr/bin/python3 ./python && \
    cp /bin/bash ./bin && \
    cd /lib/x86_64-linux-gnu && \
    cp libc.so.6 \
       libdl.so.2 \
       libexpat.so.1 \
       libm.so.6 \
       libpthread.so.0 \
       librt.so.1 \
       libutil.so.1 \
       libz.so.1 \
       /jail/zygote/lib/x86_64-linux-gnu && \
    cp /lib64/ld-linux-x86-64.so.2 /jail/zygote/lib64 && \
    cp -R /usr/lib/python3.4 /jail/zygote/usr/lib/

#    cp -R /usr/include/python3.4m /jail/zygote/usr/include/ && \

## --- 8< ----

RUN python3 -m venv /srv/appenv/py3env

WORKDIR /srv/appenv

COPY snakes/requirements.txt /srv/appenv/

RUN . /srv/appenv/py3env/bin/activate ; \
    pip install --upgrade pip==$PYTHON_PIP_VERSION && \
    pip install --no-cache-dir -r requirements.txt

COPY snakes /srv/appenv/snakes

RUN . /srv/appenv/py3env/bin/activate ; \
    cd /srv/appenv/snakes && pip install .

COPY snakes/django_snakes /srv/appenv/app

RUN . /srv/appenv/py3env/bin/activate ; \
    python -m compileall app

RUN mkdir -p /srv/appenv/app/static


## --- 8< ----

USER app

WORKDIR /srv/appenv/app

COPY docker-entrypoint.sh /_run

ENTRYPOINT ["/_run"]

CMD ["shell"]
