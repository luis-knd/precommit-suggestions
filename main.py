import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GPT_API_KEY")


def validate_php_code_from_file(file_to_evaluate):
    with open(file_to_evaluate, 'r') as php_file:
        php_code = php_file.read()
        suggestions = validate_php_code(php_code)
        return suggestions


def validate_php_code(code_to_evaluate):
    try:
        prompt_base = (
            f"Locate any logic errors, potential performance issues, suggest improvements, potential SQL injection "
            f"vulnerabilities and find any resource leaks in the following code snippet:")
        response_format = (f"Give me the answers in formal language, I don't care with the size about the response. "
                           f"However, this should be clear and included in the step by step, with clean and scalable "
                           f"code examples using the best practices and standards, and having a critical opinion. Is "
                           f"a plus translate to Spanish")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a proficient PHP, Java, Flutter, Python, and JavaScript "
                                              "developer, interested to do a better developer implemented clean code "
                                              "in my applications and use the SOLID principles."},
                {"role": "user", "content": f"{prompt_base}\n{code_to_evaluate}. {response_format}"},
            ],
            max_tokens=500,
            temperature=0
        )
        suggestions_messages = response["choices"][0]["message"]["content"]
        paragraphs = suggestions_messages.split("\n\n")
        return paragraphs
    except Exception as e:
        return str(e)


file_path = 'php/test.php'
suggestions_from_my_code = validate_php_code_from_file(file_path)
for paragraph in suggestions_from_my_code:
    print(paragraph)
