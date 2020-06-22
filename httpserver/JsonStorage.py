class JsonStorage():
  def __init__(self):
    self.dictionary = {}

  def get_value(self, key):
    if key in self.dictionary.keys():
      return (True, self.dictionary[key])

    return (False, None)

  def add_value(self, key, value):
    if key in self.dictionary.keys():
      return False
    self.dictionary[key] = value
    return True

  def alter_value(self, key, value):
    if not key in self.dictionary.keys():
      return False
    self.dictionary[key] = value
    return True

  def delete(self, key):
    if not key in self.dictionary.keys():
      return False

    del self.dictionary[key]
    return True

  def check_exists(self, key):
    return key in self.dictionary.keys()
