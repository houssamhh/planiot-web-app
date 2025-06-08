#! /bin/bash

docker build --rm --build-arg UID=$(id -u) --build-arg GID=$(id -g) --tag planiot-app:latest -f- . < dockerfile