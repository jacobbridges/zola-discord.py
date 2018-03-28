import logging


def create_standard_logger(name, filepath):
    """
    Create a standard logger which logs everything to a file and prints errors
    to the console.
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a handler which logs to a file
    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Create a handler which logs errors to the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = create_standard_logger('zola', 'zola.log')
