import logging


logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s [%(filename)s] outputNumber:[%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='a')
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    logger.warning('this is a warning')
    logger.info('this is a info')