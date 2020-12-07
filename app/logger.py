import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

FORMAT = ('%(asctime)-15s %(threadName)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
# logging.basicConfig(format=FORMAT)
# logger = logging.getLogger('cobot_app')

# logger.addHandler(handler)

path = 'logs'
logname = 'app.log'
error_logname = 'error.log'

logger = logging.getLogger('cobot_app')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(FORMAT)
logHandler = TimedRotatingFileHandler(f'{path}/{logname}', when='midnight', interval=1)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logHandler.suffix = "%Y%m%d"

errorLogHandler = TimedRotatingFileHandler(f'{path}/{error_logname}', when='midnight', interval=1)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)
logger.addHandler(streamHandler)


