from multiprocessing import get_logger
import logging


def logger(level=logging.INFO) -> logging.getLogger:
    log = get_logger()
    log.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(asctime)s - %(process)s - %(message)s'
    ))
    log.addHandler(handler)
    return log


app_logger = logger()