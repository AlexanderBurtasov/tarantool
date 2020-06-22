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
    if True == self.check_key_exist(key):
      return False

    k = self.__space.insert((key, value))
    return True

  def alter_value(self, key, value):
    if False == self.check_key_exist(key):
      return False

    self.__space.replace((key, value))
    return True

  def delete(self, key):
    if False == self.check_key_exist(key):
      return False

    self.__space.delete(key)
    return True

  def check_key_exist(self, key):
    resp = self.__space.select(key)
    return 0 != len(resp.data)
