"""
This module is used to configure the logger for an application.
It uses the logging and coloredlogs library to create and configure a logger.
"""

import logging

import coloredlogs

class CustomLogger():
    """
    This class is used to configure the logger for an application.
    It creates a logger object and sets it up with the coloredlogs library.
    """

    def __init__(self) -> None:
        """
        Initialize the ConfigLogger class.
        Creates a logger object, sets its level and configures the coloredlogs library.
        """
        # create logger
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.INFO)
        
        # log to file
        if len(self.logger.handlers) == 0:
            fileh = logging.FileHandler("latest.log", "a")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%d-%m-%Y %H:%M:%S')
            fileh.setFormatter(formatter)
            self.logger.addHandler(fileh)

        # create console handler and set level to debug
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # configure coloredlogs
        coloredlogs.DEFAULT_FIELD_STYLES = {
            'asctime': {'color': 'white'},
            'hostname': {'color': 'green'},
            'levelname': {'color': 'cyan', 'bold': True},
        }

        coloredlogs.install(level='DEBUG', logger=self.logger, handler=console_handler,
                            fmt='%(asctime)s %(levelname)s %(message)s',datefmt='%d-%m-%Y %H:%M:%S')

    def setup(self):
        """
        This method returns the setup logger object
        """
        return self.logger
