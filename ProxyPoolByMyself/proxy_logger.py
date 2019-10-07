import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s] outputNumber:[%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='ProxyPoolLog.log',
                    filemode='a')
logger = logging.getLogger(__name__)

if __name__ == "__main_":
    logger.warning('this is a log')
    logger.info('this is a info')
