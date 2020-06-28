from enum import Enum


class Defaults(Enum):
  server_url = '0.0.0.0',
  server_port = 5502,
  request_per_second = 4,
  tarantool_url = '0.0.0.0',
  tarantool_port = 3313,
  storage_name = 'mystorage'