import glob
import logging
import os
import sys

from .dao.customBaseException import CustomBaseException
from .utils.app_utils import AppUtils
from .utils.log_utils import LogUtils


class FileProcessor:
    def __init__(self, input_file, output_file, config_path, debug):
        """

        Args:
            input_file (list): Input file patten/path received from command line arguments
            output_file (str): Output file patten/path received from command line arguments
            config_path (str): Log Configuration
            debug (boolean): Debug mode

        """
        self.input_file = input_file
        self.output_file = output_file
        self.config_path = config_path
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    def process_data(self, data):
        """

        Args:
            data (str): Data read from input files

        Returns:
            str: Data after processing.
        """
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
            # Configure logging
            LogUtils.configure_logging(self.config_path)
            # project_root = os.path.abspath(os.path.dirname(__file__))
            # self.logger.info(project_root)
            # data_file_path = os.path.join(project_root, 'data', 'example.txt')

            # Data processing
            file_iterator = (filename for pattern in self.input_file for filename in glob.iglob(pattern))

            for filename in file_iterator:
                self.logger.info(f"file processing: {os.path.basename(filename)}")
                data = AppUtils.read_data(filename)
                processed_data = self.process_data(data)
                AppUtils.save_data(processed_data, self.output_file)
                self.logger.info(f"{os.path.basename(filename)} : File processing successful..!")

        except CustomBaseException as ce:
            self.logger.error(f"Custom Exception caught: {ce}")

        except Exception as exc_obj:
            exc_type, exc_tb = type(exc_obj), exc_obj.__traceback__
            template = "fileProcessor::process_file(): {1} - {2} [Line No {0}]"
            errorMessage = template.format(exc_tb.tb_lineno, exc_type.__name__, exc_obj)

            self.logger.error(f"Error : {errorMessage}")
