#!/bin/bash

# build tarantool image
docker build . -f docker/database/Dockerfile -t bugdb:0.9

# build httpserver image
docker build . -f docker/httpserver/Dockerfile -t httpserver:0.9
