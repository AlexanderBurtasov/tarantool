from http.server import BaseHTTPRequestHandler
from JsonStorage import JsonStorage
from TarantoolStorage import TarantoolStorage
import json
import re


class InnerRequestHandler(BaseHTTPRequestHandler):
  __storage = TarantoolStorage('192.168.99.100', 3301, 'storage')
#  __storage = JsonStorage()

  def do_GET(self):
    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')

    (isOk, value) = self.__storage.get_value(key)
    if True == isOk:
      self.send_json_response(200, {'message': 'ok', 'value': value})
    else:
      self.send_error(code=404, message='Record not found', explain=f'Record with a key "{key}" not found in storage')

  def do_POST(self):
    if not InnerRequestHandler.__validate_path(self.path):
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    body = self.get_body()
    values = {}
    try:
      values = json.loads(body, encoding='utf-8')
    except Exception as exc:
      self.send_json_response(400, {'message': f'Ivalid json body: {str(exc)}'})
      return

    for it in ["key", "value"]:
      if not it in values.keys():
        self.send_json_response(400, {'message': f'Missing "{it}" in incoming json'})
        return

    key = values["key"]
    isOk = self.__storage.add_value(key, values["value"])
    if not isOk:
      self.send_json_response(409, {'message': f'Value with a key "{key}" already exists'})
      return

    self.send_json_response(200, {'message': f'Value with a key "{key}" successfully added'})

  def do_PUT(self):
    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    body = self.get_body()
    values = {}
    try:
      values = json.loads(body, encoding='utf-8')
    except Exception as exc:
      self.send_json_response(400, {'message': f'Ivalid json body: {str(exc)}'})
      return

    if not self.__storage.check_key_exist(key):
      self.send_error(code=404, message='Record not found', explain=f'Record with a key "{key}" not found in storage')
      return

    for it in ["value"]:
      if not it in values.keys():
        self.send_json_response(400, {'message': f'Missing "{it}" in incoming json'})
        return

    if not self.__storage.alter_value(key, values["value"]):
      self.send_json_response(409, {'message': f'Cannot alter value with a key "{key}"'})
      return
    self.send_json_response(200, {'message': f'Value with a key "{key}" changed'})

  def do_DELETE(self):
    (isOk, key) = InnerRequestHandler.__extract_key_from_path(self.path)
    if not isOk:
      self.send_error(code=404, message='Path not found', explain=f'Path {self.command} {self.path} not exists')
      return

    if not self.__storage.check_key_exist(key):
      self.send_error(code=404, message='Record not found', explain=f'Record with a key "{key}" not found in storage')
      return

    if not self.__storage.delete(key):
      self.send_json_response(409, {'message': f'Cannot remove value with a key "{key}" from storage'})
      return

    self.send_json_response(200, {'message': f'Value with a key "{key}" deleted'})

  def get_body(self):
    content_len = int(self.headers.get('Content-Length'))
    return self.rfile.read(content_len)

  def send_json_response(self, code, json_values):
    response_body = json.dumps(json_values).encode(encoding='utf-8')
    self.send_response(code=code)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(response_body)

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
