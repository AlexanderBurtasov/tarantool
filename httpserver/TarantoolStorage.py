import tarantool


class TarantoolStorage():
  def __init__(self, host, port, space):
    self.__connection = tarantool.connect(host, port)
    self.__space = self.__connection.space(space)

  def get_value(self, key):
    resp = self.__space.select(key)
    if 0 == resp.return_code and 1 == len(resp.data):
      return (True, resp.data[0][1])

    return (False, None)

  def add_value(self, key, value):
    try:
      self.__space.insert((key, value))
      return (True, '')
    except tarantool.error.DatabaseError as err:
      return (False, err.args[1])

  def alter_value(self, key, value):
    try:
      result = self.__space.update(key, [('=', 1, value)])
      if 0 == len(result.data):
        return (False, f'Value with key "{key}" not exists')

      return (True, '')
    except tarantool.error.DatabaseError as err:
      return (False, err.args[1])

  def delete(self, key):
    result = self.__space.delete(key)
    if 0 == len(result.data):
      return (False, f'Value with key "{key}" not exists')

    return (True, '')

  def check_key_exist(self, key):
    result = self.__space.select(key)
    return 0 != len(result.data)
