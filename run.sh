#!/bin/bash

docker run --name bugcontainer -p 3313:3313 bugdb:0.9
docker run --name httpservercontainer -p 5052:5052 httpserver:0.9
