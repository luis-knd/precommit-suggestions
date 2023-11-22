import logging
import os
import shutil
import time

import openai
from dotenv import load_dotenv

from src.gpt_constants import Gpt
load_dotenv()


class GPTConnection:

    def __init__(self):
        self.api_key = os.getenv("GPT_API_KEY")
        openai.api_key = self.api_key

    def validate_changes_in_code_from_file(self, all_edited_files, directory_path):
        suggestions = ""
        for file_to_evaluate in all_edited_files:
            logging.info(f"I will to evaluate: {file_to_evaluate}")
            filename, extension = os.path.splitext(os.path.basename(file_to_evaluate))
            suggestions += f"FILE: {filename}\n"
            with open(file_to_evaluate, 'r') as issue_file:
                changes_in_code = issue_file.read()
                suggestion_paragraphs = self.validate_changes_in_code(changes_in_code)
                for paragraph in suggestion_paragraphs:
                    suggestions += f"{paragraph}\n"
                suggestions += "\n--------------------------------------------------------------------------------\n\n"
        shutil.rmtree(directory_path)
        return suggestions

    @staticmethod
    def validate_changes_in_code(code_to_evaluate):
        try:
            prompt_base = (
                f"Locate any logic errors, potential performance issues, suggest improvements, potential SQL injection "
                f"vulnerabilities and find any resource leaks in the following code snippet:")
            response_format = (f"Give me the answers in formal language, I don't care with the size about the "
                               f"response. However, this should be clear and included in the step by step, "
                               f"with clean and scalable code examples using the best practices and standards, "
                               f"OWASP rules and having a critical opinion. Translate to Spanish")
            logging.info("preparing the query to GPT in search of logical errors and performance problems")
            start_time = time.time()
            # TODO comment this for not use all my Free request
            # response = "PRUEBA de una respuesta de ChatGpt "
            # suggestions_messages = response
            response = openai.ChatCompletion.create(
                model=Gpt.MODEL_GPT_4.value,
                messages=[
                    {"role": "system", "content": "You are a proficient PHP, Java, Flutter, Python, C# and JavaScript "
                                                  "developer, interested to do a better developer implemented clean "
                                                  "code in my applications and use the SOLID principles."},
                    {"role": "user", "content": f"{prompt_base}\n{code_to_evaluate}. {response_format}"},
                ],
                max_tokens=1500,
                temperature=0
            )
            end_time = time.time()
            suggestions_messages = response["choices"][0]["message"]["content"]
            paragraphs = suggestions_messages.split("\n\n")
            logging.info(f"we already have a suggestion from GPT, the same delay: {end_time - start_time:.2f} seconds.")
            return paragraphs
        except Exception as e:
            logging.error(f"an error occurred: {e}")
            return str(f"an error occurred: {e}")
