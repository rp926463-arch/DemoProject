import logging.config
import json


class LogUtils:

    @staticmethod
    def logger():
        """
        Provide loggers to all utils modules

        """
        logger = logging.getLogger(__name__)
        return logger

    @staticmethod
    def load_logging_config(config_path='config/logging_config.json'):
        """
        Load logging configuration from the specified file path.

        Args:
            config_path (str): Path to the logging configuration file.

        Returns:
            dict: Logging configuration loaded from the file.
        """
        with open(config_path, 'rt') as f:
            logging_config = json.load(f)
        return logging_config

    @staticmethod
    def configure_logging(logging_config):
        """
        Configure logging using the provided logging configuration.

        Args:
            logging_config (dict): Logging configuration.
        """
        logging.config.dictConfig(logging_config)
