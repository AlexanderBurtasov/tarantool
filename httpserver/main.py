from http.server import HTTPServer
from InnerRequestHandler import InnerRequestHandler
import logutils

def main():
  logutils.initLogger('logs')

  httpd = HTTPServer(('localhost', 5052), InnerRequestHandler)
  httpd.serve_forever()

  return 0


if __name__ == '__main__':
  result = main()
