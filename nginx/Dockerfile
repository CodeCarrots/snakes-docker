FROM debian:jessie

ENV NGINX_VERSION=1.6.2-5+deb8u1

RUN apt-get update && \
    apt-get install -o APT::Install-Recommends=false \
                    -o APT::Install-Suggests=false -y \
                    nginx=${NGINX_VERSION} nginx-light=${NGINX_VERSION} && \
    apt-get clean && \
    rm -Rf /var/lib/apt/lists/*

RUN rm -f /etc/nginx/sites-enabled/default

ADD nginx-app /etc/nginx/sites-enabled/

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

VOLUME ["/var/cache/nginx"]

EXPOSE 80

RUN mkdir -p /srv/appenv/app

ADD static.tar /srv/appenv/app/

CMD ["nginx", "-g", "daemon off;"]
