import logging
from dao.customBaseException import CustomBaseException


class AppUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def read_data(file_path):
        """
        Reads data from a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file.

        Raises:
            CustomBaseException: If an error occurs during file reading.
        """
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            AppUtils.logger.info("data read successfully..")
            return data

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::read_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error reading file: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def save_data(processed_data, file_path):
        """
        Saves processed data to a file.

        Args:
            processed_data (str): The data to be saved.
            file_path (str): The path to the file.

        Raises:
            CustomBaseException: If an error occurs during file writing.
        """
        try:
            with open(file_path, 'a') as file:
                file.write(processed_data)

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "app_utils::save_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            AppUtils.logger.error(f"Error saving data to file: {exc_obj}")
            raise CustomBaseException(errorMessage)
