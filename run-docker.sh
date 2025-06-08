#! /bin/bash

docker run -it --rm -p 8501:8501 -v $(pwd):/home/planiot/planiot -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /tmp/.docker.xauth:/tmp/.docker.xauth --env=DISPLAY=host.docker.internal:0.0 --env=XAUTHORITY=/tmp/.docker.xauth planiot