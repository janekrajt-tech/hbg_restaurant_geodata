import logging 

LOGGER_NAME = "validate_data"


def configure_logging() -> None:
    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("logs/validation.log")
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    file_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False