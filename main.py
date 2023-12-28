import argparse
from app.fileProcessor import FileProcessor
import os


def main(input_file_path, output_file_path, debug):
    """

    Args:
            input_file_path (list): Input file patten/path received from command line arguments
            output_file_path (str): Output file patten/path received from command line arguments
            debug (boolean): Debug mode
    """
    # Use absolute paths for configuration and data files
    config_path = os.path.abspath('config/logging_config.json')

    # Process the file
    file_processor = FileProcessor(input_file_path, output_file_path, config_path, debug)
    file_processor.process_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 2.0')
    parser.add_argument('--infile', '-i', required=True, nargs='+')
    parser.add_argument('--outfile', '-o', required=True, type=str)
    parser.add_argument('--debug', '-d', nargs='?', const=1, default=0)
    args = parser.parse_args()
    print(f"Arguments received : {args}")

    main(args.infile, args.outfile, args.debug)

# python main.py -i "data/i*.txt" "data/o*.txt" -o "data/output.txt"
# python main.py -i "data/input.txt" "data/output.txt" -o "data/output.txt"
# python main.py -i "data/input.txt" "data/output.txt" -o "data/output.txt" -d
