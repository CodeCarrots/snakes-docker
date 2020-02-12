#!/usr/bin/env bash

set -Eeuo pipefail

docker-compose up --force-recreate --build --remove-orphans --abort-on-container-exit
