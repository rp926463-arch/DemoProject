import logging.config
import json
from demo_project.app.dao.customBaseException import CustomBaseException


class LogUtils:
    logger = logging.getLogger(__name__)

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

            LogUtils.logger.error(f"Error loading log config: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        return logger

    @staticmethod
    def configure_logging(config_path):

        """
        Configure logging using the provided or default logging configuration.

        Args:
            config_path (str): Path to the logging configuration file.
        """
        try:
            logging_config = LogUtils.load_logging_config(config_path)
            logging.config.dictConfig(logging_config)
            LogUtils.logger.info("Logging configured.")

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "log_utils::configure_logging(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            LogUtils.logger.error(f"Error configuring log config: {exc_obj}")
            raise CustomBaseException(errorMessage)
