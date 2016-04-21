import json
import ast

input_file = open("my_data.json", 'r')

content = input_file.read()

input_file.close()

list_content = ast.literal_eval(content)






	