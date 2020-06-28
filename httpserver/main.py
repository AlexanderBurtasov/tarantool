from http.server import HTTPServer
from argparse import ArgumentParser
from InnerRequestHandler import InnerRequestHandler
from defaults import Defaults
from TarantoolStorage import TarantoolStorage
from RequestTimer import RequestTimer
import logutils


class RunParam:
  def __init__(self, parse_args):
    self.server_url = parse_args.server_url or Defaults.server_url.value[0]
    self.server_port = parse_args.server_port or Defaults.server_port.value[0]
    self.request_per_second = parse_args.request_per_second or Defaults.request_per_second.value[0]
    self.tarantool_url = parse_args.tarantool_url or Defaults.tarantool_url.value[0]
    self.tarantool_port = parse_args.tarantool_port or Defaults.tarantool_port.value[0]

  def trace(self):
    return f'server:    url: {self.server_url}, port: {self.server_port}, max requests per second: {self.request_per_second}\n' \
           f'tarantool: url: {self.tarantool_url}, port: {self.tarantool_port}'

def parse_command_line():
  # parse input arguments
  parser = ArgumentParser(description='run httpserver with tarantool arguments')
  parser.add_argument('--server-url', dest='server_url', action='store', help='Http server URL', type=str)
  parser.add_argument('--server-port', dest='server_port', help='Http server port number', type=int)
  parser.add_argument('--request-per-second', dest='request_per_second',
                      help='Server requests per second maximum count', type=int)
  parser.add_argument('--tarantool-url', dest='tarantool_url', help='Tarantool database URL', type=str)
  parser.add_argument('--tarantool-port', dest='tarantool_port', help='Tarantool database port number', type=int)
  parse_args = parser.parse_args()

  return RunParam(parse_args)


def main():
  logutils.initLogger('logs')
  runParam = parse_command_line()
  print(runParam.trace())

  try:
    bugStorage = TarantoolStorage(runParam.tarantool_url, runParam.tarantool_port, Defaults.storage_name.value)
    requestTimer = RequestTimer(runParam.request_per_second)

    httpServer = HTTPServer((runParam.server_url, runParam.server_port), InnerRequestHandler)
    httpServer.bugStorage = bugStorage
    httpServer.requestTimer = requestTimer

    httpServer.serve_forever()
  except Exception as exc:
    print('Error running server: {0}'.format(str(exc)))

  return 0


if __name__ == '__main__':
  result = main()
