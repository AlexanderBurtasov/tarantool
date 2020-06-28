from http.server import BaseHTTPRequestHandler
from TarantoolStorage import TarantoolStorage
from RequestTimer import RequestTimer
from defaults import Defaults
import json
import logging
import re


class InnerRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    logger = logging.getLogger()
    logger.info(f'GET {self.path}')

    if not self.__accept():
      return

    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')

    (isOk, value) = self.server.bugStorage.get_value(key)
    if True == isOk:
      self.__send_json_response(200, {'key': key, 'value': value})
    else:
      self.send_error(code=404, message='Record not found', explain=f'Record with a key "{key}" not found in storage')

  def do_POST(self):
    body = self.__get_body()

    logger = logging.getLogger()
    logger.info(f'POST {self.path} {body}')

    if not self.__accept():
      return

    if not InnerRequestHandler.__validate_path(self.path):
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    values = {}
    try:
      values = json.loads(body, encoding='utf-8')
    except Exception as exc:
      self.send_error(code=400, message='Invalid json body', explain=str(exc))
      return

    for it in ["key", "value"]:
      if not it in values.keys():
        self.send_error(code=400, message='Invalid json body', explain=f'Missing "{it}" section in source json')
        return

    key = values["key"]
    (isOk, message) = self.server.bugStorage.add_value(key, values["value"])
    if not isOk:
      self.send_error(code=409, message=f'Cannot add key "{key}"', explain=message)
      return

    self.__send_json_response(200, {'message': f'Value with key "{key}" successfully added'})

  def do_PUT(self):
    body = self.__get_body()
    logger = logging.getLogger()
    logger.info(f'PUT {self.path} {body}')

    if not self.__accept():
      return

    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    (isOk, values, errorMsg) = InnerRequestHandler.__parse_json_body(body=body)
    if not isOk:
      self.send_error(code=400, message='Invalid json body', explain=errorMsg)
      return

    for it in ["value"]:
      if not it in values.keys():
        self.send_error(code=400, message='Invalid json body', explain=f'Missing "{it}" section in source json')
        return

    (isOk, message) = self.server.bugStorage.alter_value(key, values["value"])
    if not isOk:
      self.send_error(404, message=f'Cannot alter value with key "{key}"', explain=message)
      return
    self.__send_json_response(200, {'message': f'Value with key "{key}" changed'})

  def do_DELETE(self):
    logger = logging.getLogger()
    logger.info(f'DELETE {self.path}')

    if not self.__accept():
      return

    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    (isOk, message) = self.server.bugStorage.delete(key)
    if not isOk:
      self.send_error(code=404, message=f'Cannot delete key "{key}"', explain=message)
      return

    self.__send_json_response(200, {'message': f'Value with a key "{key}" deleted'})

  def __get_body(self):
    content_len = int(self.headers.get('Content-Length'))
    return self.rfile.read(content_len)

  def __send_json_response(self, code, json_values):
    logger = logging.getLogger()
    logger.info(f'code: {code}; {json_values}')
    response_body = json.dumps(json_values).encode(encoding='utf-8')
    self.send_response(code=code)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(response_body)

  def __accept(self):
    if not self.server.requestTimer.accept():
      self.send_error(code=429, message='Too many requests', explain='Requests per second count exceeded')
      return False
    return True

  def send_error(self, code, message, explain):
    logger = logging.getLogger()
    logger.warning(f'code: {code}; message: {message}; explain: {explain}')
    super().send_error(code=code, message=message, explain=explain)

  @staticmethod
  def __parse_json_body(body):
    values = {}
    try:
      values = json.loads(body, encoding='utf-8')
    except Exception as exc:
      return (False, {}, str(exc))
    return (True, values, '')

  @staticmethod
  def __validate_path(path):
    regExp = re.compile('(\\/kv)', re.IGNORECASE)
    return regExp.fullmatch(path)

  @staticmethod
  def __extract_key_from_path(path):
    regExp = re.compile('(\\/kv)(\\/)(.+)', re.IGNORECASE)
    matchResults = regExp.match(path)
    if None == matchResults:
      return (False, None)
    if 3 != matchResults.lastindex:
      return (False, None)

    return (True, matchResults[3])
