from proxy_logger import logger
from proxypool.scheduler import Scheduler


def main():
    LOGGER = logger
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        LOGGER.debug(e)
        print('main.py raise a error: {}'.format(e))

if __name__ == "__main__":
    main()