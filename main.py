import logging
from datetime import datetime

from src.classes.gpt_connection import GPTConnection
from src.classes.jira_connection import JiraAPI

logging.basicConfig(filename=f"src/data/logs/log_file_{datetime.now().strftime('%Y%m')}.log", level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S%p')
logging.info("--------------------------------------------------")
logging.info("I start the process of consulting code suggestions with Gpt")

gpt_connection = GPTConnection()
# TODO that values (test.php) should be set from git diff
file_path = 'src/data/php/test.php'
suggestions_from_my_code = gpt_connection.validate_php_code_from_file(file_path)

# TODO this value (NUM_DE_JIRA) should be set from git
file_name = f"NUM_DE_JIRA_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
file_path = f"src/data/cr_suggestions/{file_name}"

logging.info(f"the file for the CR was generated: {file_name}")
with open(file_path, 'w', encoding="utf-8") as file:
    for paragraph in suggestions_from_my_code:
        file.write(f"{paragraph}\n")

jira = JiraAPI()
jira.add_attachments_issue("BDEV-68", file_path)
jira.comment_issue("BDEV-68", "Esta es una sugerencia a tu cambio autogenerada por ChatGpt.", file_name)

logging.info("end of the process of consulting code suggestions with Gpt")
logging.info("--------------------------------------------------\n\n")
