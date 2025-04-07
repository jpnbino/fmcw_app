import logging

# Logging level (adjust as needed)
LOG_LEVEL = logging.INFO

# Log format (customize for your needs)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def configure_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
