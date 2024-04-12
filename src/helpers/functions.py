import argparse
import logging
import os
import re
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging():
    """
    Setup logging configuration.

    This function configures the logging module to log messages to a file with a specific format and rotation settings.

    :return: None
    """

    logs_dir = 'src/data/logs'
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = f"{logs_dir}/log_file_{datetime.now().strftime('%Y%m')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S%p',
        handlers=[
            logging.FileHandler(log_file_path),
            RotatingFileHandler(log_file_path, maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ]
    )


def parse_command_line_arguments():
    """
    Parse the command line arguments.

    :return: Tuple containing the parsed Jira key and input file.
    :rtype: tuple[str, str]
    """
    parser = argparse.ArgumentParser(description='Process Jira key and input file.')
    parser.add_argument('jira_key', type=str, help='Jira key for the task')
    parser.add_argument('input_file', type=str, help='Input file')
    args = parser.parse_args()

    return args.jira_key, args.input_file


def parse_git_diff_file(input_file):
    """
    Parses a Git diff file and extracts information into separate text files.

    :param input_file: Path to the Git diff file.
    """
    try:
        logging.info(f"input_file: {input_file}")
        with open(input_file, 'r') as file:
            file_content = file.read()

        file_sections = re.split(r'diff --git', file_content)[1:]

        for section in file_sections:
            parsed_content = ""
            lines = section.strip().split('\n')
            file_info = lines[0].split()
            file_name = file_info[-1]

            code_lines = lines[1:]
            code_block_started = False
            for line in code_lines:
                if line.startswith('@@'):
                    code_block_started = True
                    continue

                if line.startswith('-'):
                    continue

                if code_block_started:
                    if line.startswith('+'):
                        parsed_content += f" {line[1:]}\n"
                    else:
                        parsed_content += line + '\n'
            parsed_content += "\n"

            output_file_path = os.path.join(os.path.dirname(input_file), os.path.basename(file_name[2:]) + ".txt")
            with open(output_file_path, 'w') as specific_file:
                specific_file.write(parsed_content)
        os.remove(input_file)
    except FileNotFoundError as e:
        logging.error(f"file not found: {e}")
    except PermissionError as e:
        logging.error(f"permission error: {e}")
    except Exception as e:
        logging.error(f"an unexpected error occurred: {e}")


def get_all_files_in_path(directory):
    """
    Get a list of all files in the specified directory.

    :param directory: Path to the directory.
    :return: List of file paths.
    """
    try:
        all_files = os.listdir(directory)

        # Use a list comprehension to filter out only files (not directories)
        file_paths = [
            os.path.join(directory, file)
            for file in all_files
            if os.path.isfile(os.path.join(directory, file))
        ]

        return file_paths

    except OSError as e:
        # Handle potential errors, e.g., if the specified path does not exist
        logging.error(f"an error ocurred: {e}")
        return []
