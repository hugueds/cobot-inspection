import logging
from logger import logger


def run():
    logger.info('OK')
    logger.warning('Warning')
    logger.warn('Warn')
    logger.error('Error')
    for i in range(1000):        
        logger.error('Error ' + str(i))
