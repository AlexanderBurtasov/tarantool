#!/bin/bash

python3 main.py --server-url ${SERVER_URL} --server-port ${SERVER_PORT} --request-per-second ${REQUEST_PER_SECOND} --tarantool-url ${TARANTOOL_URL} --tarantool-port ${TARANTOOL_PORT}
