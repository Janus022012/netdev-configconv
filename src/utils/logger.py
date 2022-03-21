import logging


def get_custom_logger(name: str):
    return get_info_logger(name)


def get_info_logger(name: str):
    info_logger = logging.getLogger(name)
    info_logger.setLevel(logging.INFO)
    info_handler = logging.StreamHandler()
    info_handler.setFormatter(logging.Formatter("%(levelname)-6s message=%(message)s"))
    info_handler.setLevel(logging.INFO)
    info_logger.addHandler(info_handler)

    return info_logger


def get_debug_logger(name: str):
    debug_logger = logging.getLogger(name)
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.StreamHandler()
    debug_handler.setFormatter(logging.Formatter("level=%(levelname)-6s place=%(name)s %(funcName)s() Line%(lineno)-4d message=%(message)s"))
    debug_handler.setLevel(logging.DEBUG)
    debug_logger.addHandler(debug_handler)

    return debug_logger

