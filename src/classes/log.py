import logging
from datetime import datetime


class Logger:
    def __init__(self):
        self.filename = self.generate_log_filename()
        self.logger = self.create_logger()

    @staticmethod
    def generate_log_filename():
        return f"src/data/logs/log_file_{datetime.now().strftime('%Y%m')}.log"

    def create_logger(self):
        logger = logging.getLogger(self.filename)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler(self.filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def log(self, message, error=False):
        if error:
            self.logger.error(message)
        else:
            self.logger.info(message)
