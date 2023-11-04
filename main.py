from api.gpt_connection import GPTConnection

gpt_connection = GPTConnection()
file_path = 'data/php/test.php'
suggestions_from_my_code = gpt_connection.validate_php_code_from_file(file_path)
for paragraph in suggestions_from_my_code:
    print(paragraph)
