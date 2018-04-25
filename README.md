snakes-docker
=============

Set of helper files to set-up Docker images and environment for
running the [snakes](https://github.com/CodeCarrots/snakes.git)
server. The main server code is included here as a git submodule, so
you might need something like:

      $ git pull && git fetch -t -p && git submodule update


Note
----

This repo is not click'n'forget. fix_config.* are the entry point -
docker-compose-like environment description files (just with a Python
syntax, something a hypothetical/unreleased mini Docker orchestration
tool might use) but then you're mostly on your own.

Also, this setup was created around May 2016.
