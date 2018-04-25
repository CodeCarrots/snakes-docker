from fix import Image, Volume, Network, Service, Project
from fix import copy_into_context, wait_until
from fix.templates import render_into_context


class snakes(Project):
    net_db = Network()
    net_front = Network()

    volume_db = Volume()

    img_redis = Image(image_name='redis', tag='3.0')
    img_app = Image()
    img_nginx = Image()

    redis = Service(
        image = img_redis,
        restart = 'always',
        networks = [net_db],
        volumes = {volume_db: '/data'},
    )

    snakes = Service(
        image = img_app,
        restart = 'always',
        networks = [net_db],
        env = {
            'REDIS_HOST': redis,
        },
        user = 0,
        cap_add = ['SYS_ADMIN', 'MKNOD'],
        # temp fix for ubuntu here, shouldn't be needed on debian for now
        # privileged = True,
        command = 'snakes-run',
        for_started_set = wait_until(redis, 'running')
    )

    django = Service(
        image = img_app,
        restart = 'always',
        networks = [net_db, net_front],
        env = {
            'REDIS_HOST': redis,
            'SECRET_KEY': 'thisIsNotARealSecretKeyReally',
        },
        command = 'django-run',
        for_started_set = wait_until(redis, 'running')
    )

    nginx = Service(
        image = img_nginx,
        restart = 'always',
        networks = [net_front],
        ports = {80: 80},
        for_started_set = wait_until(django, 'running'),
    )

    class Meta:
        registry = 'localhost:5000'
        repository = 'carrots'
        name = 'snakes'
