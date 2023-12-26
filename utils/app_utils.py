from utils.log_utils import LogUtils
from dao.customBaseException import CustomBaseException


class AppUtils:

    @staticmethod
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            LogUtils.logger().info("data read successfully..")
            return data
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "fileReader::read_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            LogUtils.logger().error(f"Error reading file: {exc_obj}")
            raise CustomBaseException(errorMessage)

    @staticmethod
    def save_data(processed_data, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write(processed_data)
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "fileWriter::save_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            LogUtils.logger().error(f"Error saving data to file: {exc_obj}")
            raise CustomBaseException(errorMessage)
