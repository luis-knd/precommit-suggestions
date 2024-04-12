import logging
import os
import sys
from datetime import datetime

from src.classes.gpt_connection import GPTConnection
from src.classes.jira_connection import JiraAPI
from src.helpers.functions import (setup_logging, parse_command_line_arguments, parse_git_diff_file,
                                   get_all_files_in_path)


if __name__ == "__main__":
    setup_logging()
    logging.info("--------------------------------------------------")

    logging.info("checking the correct value from the start parameters")
    try:
        jira_key, input_file = parse_command_line_arguments()
        if not (jira_key and input_file):
            raise ValueError("jira key and input file are required.")
    except Exception as e:
        logging.error(f"an error occurred while parsing command line arguments: {e}")
        sys.exit(1)

    directory_path = os.path.dirname(input_file)

    logging.info(f"cleaning the git diff file for the Jira task: {jira_key}")
    parse_git_diff_file(input_file)

    logging.info("obtain all edit files")
    all_edited_files = get_all_files_in_path(directory_path)

    logging.info("starting the process of consulting code suggestions with Gpt")
    gpt_connection = GPTConnection()
    suggestions_from_my_code = gpt_connection.validate_changes_in_code_from_file(all_edited_files, directory_path)

    file_name = f"{jira_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    relative_file_path = f"src/data/cr_suggestions/{file_name}"
    file_path = os.path.abspath(relative_file_path)

    logging.info(f"validate if exist and create if the directory file {file_path} doesn't exist")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    logging.info(f"the file for the CR was generated: {file_name}")
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(suggestions_from_my_code)
    except Exception as e:
        logging.error(f"an error occurred while writing to the file: {e}")
        sys.exit(1)

    jira = JiraAPI()
    jira.add_attachments_issue(jira_key, file_path)
    jira.comment_issue(jira_key, "Esta es una sugerencia a tu cambio autogenerada por ChatGpt.", file_name)

    logging.info("end of the process of consulting code suggestions with Gpt")
    logging.info("--------------------------------------------------\n\n")
