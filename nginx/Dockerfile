FROM nginx:1.16-alpine

ENV \
    PORT=8000 \
    EXP_HTTP_PORT=80 \
    LANG=C.UTF-8

WORKDIR /var/empty

ADD nginx-app /etc/nginx/

RUN \
    envsubst '${PORT} ${EXP_HTTP_PORT}' < /etc/nginx/nginx-app > /etc/nginx/conf.d/default.conf

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /srv/appenv/app/static

HEALTHCHECK \
    --interval=3m14s --timeout=10s --start-period=42s --retries=3 \
    CMD curl -f http://localhost:${EXP_HTTP_PORT}/ || exit 1

VOLUME ["/var/cache/nginx"]

EXPOSE ${EXP_HTTP_PORT}

ENTRYPOINT ["nginx"]

CMD ["-g", "daemon off;"]
