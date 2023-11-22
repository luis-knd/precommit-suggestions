import logging
import os
import sys
from datetime import datetime

from src.classes.gpt_connection import GPTConnection
from src.classes.jira_connection import JiraAPI
from src.helpers.functions import parse_git_diff_file, get_all_files_in_path

if __name__ == "__main__":
    logging.basicConfig(filename=f"src/data/logs/log_file_{datetime.now().strftime('%Y%m')}.log", level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S%p')
    logging.info("--------------------------------------------------")

    logging.info("checking the correct value from the start parameters")
    if len(sys.argv) < 3 or sys.argv[1] == "":
        logging.error("an error ocurred <jira_key> <input_file>")
        sys.exit(1)

    jira_key = sys.argv[1]
    input_file = sys.argv[2]
    directory_path = os.path.dirname(input_file)

    logging.info(f"cleaning the git diff file for the Jira task: {jira_key}")
    parse_git_diff_file(input_file)

    logging.info("obtain all edit files")
    all_edited_files = get_all_files_in_path(directory_path)

    logging.info("starting the process of consulting code suggestions with Gpt")
    gpt_connection = GPTConnection()
    suggestions_from_my_code = gpt_connection.validate_changes_in_code_from_file(all_edited_files, directory_path)

    file_name = f"{jira_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    file_path = f"src/data/cr_suggestions/{file_name}"

    logging.info(f"the file for the CR was generated: {file_name}")
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(suggestions_from_my_code)

    jira = JiraAPI()
    jira.add_attachments_issue(jira_key, file_path)
    jira.comment_issue(jira_key, "Esta es una sugerencia a tu cambio autogenerada por ChatGpt.", file_name)

    logging.info("end of the process of consulting code suggestions with Gpt")
    logging.info("--------------------------------------------------\n\n")
