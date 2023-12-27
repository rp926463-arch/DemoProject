from app.fileProcessor import FileProcessor
import os


def main():
    input_file_path = "../data/input.txt"
    output_file_path = "../data/output.txt"

    # Use absolute paths for configuration and data files
    config_path = os.path.abspath('../config/logging_config.json')

    # Process the file
    file_processor = FileProcessor(input_file_path, output_file_path, config_path)
    file_processor.process_file()


if __name__ == "__main__":
    main()
