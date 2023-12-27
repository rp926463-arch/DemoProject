import logging.config
import json
from dao.customBaseException import CustomBaseException


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
        try:
            with open(config_path, 'rt') as f:
                logging_config = json.load(f)
            return logging_config
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "log_utils::load_logging_config(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            LogUtils.logger().error(f"Error loading log config: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def configure_logging(logging_config):
        """
        Configure logging using the provided logging configuration.

        Args:
            logging_config (dict): Logging configuration.
        """
        logging.config.dictConfig(logging_config)
