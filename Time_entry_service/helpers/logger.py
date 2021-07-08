import logging

def initialize_logger(app):
    logger = logging.getLogger(__name__)
    logger.info("Initializing the logger file")