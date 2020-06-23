from time import time

class RequestTimer():
  def __init__(self, requests_per_second):
    self.__min_delta_microsend = 0
    if requests_per_second > 0:
      self.__min_delta_microsend = 1000000 / requests_per_second
    self.__lastAccept = RequestTimer.__get_microseconds()

  def accept(self):
    now = RequestTimer.__get_microseconds()
    timeDelta = now - self.__lastAccept
    if self.__min_delta_microsend < timeDelta:
      self.__lastAccept = now
      return True

    return False

  @staticmethod
  def __get_microseconds():
    return int(time() * 1000000)
