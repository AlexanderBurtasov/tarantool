from http.server import HTTPServer
from InnerRequestHandler import InnerRequestHandler

import tarantool


def main():
  httpd = HTTPServer(('localhost', 5052), InnerRequestHandler)
  httpd.serve_forever()
  return 0

def test_tarantool():
  connection = tarantool.connect("192.168.99.100", 3301)
  tester = connection.space('tester')
  a = tester.select()
  k = 0
  k = k + 1


if __name__ == '__main__':
  #test_tarantool()
  result = main()
