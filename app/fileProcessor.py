import logging
from dao.customBaseException import CustomBaseException
from utils.app_utils import AppUtils


class FileProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.logger = logging.getLogger(__name__)

    def process_data(self, data):
        try:
            # Example: Convert data to uppercase
            processed_data = data.upper()
            return processed_data
        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "dataProcessor::process_data(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            self.logger.error(f"Error processing data: {exc_obj}")
            raise CustomBaseException(errorMessage)

    def process_file(self):
        try:
            data = AppUtils.read_data(self.input_file)
            processed_data = self.process_data(data)
            AppUtils.save_data(processed_data, self.output_file)
            self.logger.info("File processing successful!")

        except CustomBaseException as ce:
            self.logger.error(f"Custom Exception caught: {ce}")

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "fileProcessor::process_file(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            self.logger.error(f"Unknown exception : {errorMessage}")



