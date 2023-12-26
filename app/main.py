from app.fileProcessor import FileProcessor
from utils.log_utils import LogUtils
import os


def main():
    input_file_path = "../data/input.txt"
    output_file_path = "../data/output.txt"

    file_processor = FileProcessor(input_file_path, output_file_path)
    file_processor.process_file()


if __name__ == "__main__":
    # Use absolute paths for configuration and data files
    config_path = os.path.abspath('../config/logging_config.json')

    # Load logging configuration
    logging_config = LogUtils.load_logging_config(config_path)

    # Configure logging
    LogUtils.configure_logging(logging_config)
    main()
