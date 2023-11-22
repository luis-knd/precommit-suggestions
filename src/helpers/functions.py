import logging
import os
import re


def parse_git_diff_file(input_file):
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
        with open(f"{os.path.dirname(input_file)}/{os.path.basename(file_name[2:])}.txt", 'w') as specific_file:
            logging.info(input_file)
            logging.info(parsed_content)
            specific_file.write(parsed_content)
    os.remove(input_file)


def get_all_files_in_path(directory):
    try:
        all_files = os.listdir(directory)

        # Use a list comprehension to filter out only files (not directories)
        file_paths = [os.path.join(directory, file) for file in all_files if os.path.isfile(os.path.join(directory, file))]

        return file_paths

    except OSError as e:
        # Handle potential errors, e.g., if the specified path does not exist
        logging.error(f"an error ocurred: {e}")
        return []
