import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
