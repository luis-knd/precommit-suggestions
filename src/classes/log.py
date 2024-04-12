import logging
from datetime import datetime


class Logger:
    """
    Logger class

    The Logger class is used to create and manage log files for logging information and errors.

    Attributes:
        filename (str): The name of the log file.
        logger (logging.Logger): The logger object to handle logging operations.

    Methods:
        generate_log_filename: Generates the name of the log file based on the current date and time.
        create_logger: Creates the logger object with the specified log file and logging level.
        log: Logs the provided message with the specified logging level.

    Example usage:
        logger = Logger()
        logger.log("This is a log message")
    """
    def __init__(self):
        self.filename = self.generate_log_filename()
        self.logger = self.create_logger()

    @staticmethod
    def generate_log_filename():
        """
        Generate a log filename based on the current date and time.

        :return: A string representing the generated log filename.
        """
        return f"src/data/logs/log_file_{datetime.now().strftime('%Y%m')}.log"

    def create_logger(self):
        """
        Creates and configures a logger object.

        :return: A logger object that can be used to log messages to a file.
        """
        logger = logging.getLogger(self.filename)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler(self.filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def log(self, message, error=False):
        """
        :param message: The message to be logged (string)
        :param error: Flag indicating whether the log is an error or not (boolean)
        :return: None

        Logs a message with an optional error flag. If the error flag is True, the message will be logged as an error
        level message. If the error flag is False, the message will be logged as an info level message.

        Example usage:
            logger = Logger()
            logger.log("This is an info log")
            logger.log("This is an error log", error=True)
        """
        if error:
            self.logger.error(message)
        else:
            self.logger.info(message)
