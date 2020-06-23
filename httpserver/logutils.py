from datetime import datetime, timedelta
import logging
import os

def initLogger(dirPath):
  try:
    if not os.path.exists(dirPath) or not os.path.isdir(dirPath):
      os.mkdir(dirPath)

    fileName = os.path.join(dirPath, "{0}.log".format(datetime.now().strftime("%Y-%m-%d %H.%M.%S")))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler(fileName)
    formatter = logging.Formatter("[%(asctime)s];[%(name)s];[%(levelname)s];%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fileHandler.setFormatter(formatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

  except OSError as exc:
    print('Cannot create logger: {0}'.format(exc.strerror))
