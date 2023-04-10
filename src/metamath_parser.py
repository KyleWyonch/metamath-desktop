import os
import re

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def tokenize(content):
    return [token.strip() for token in re.findall(r'\S+|\n', content)]

def parse_tokens(tokens):
    header = []
    in_header = False

    for token in tokens:
        if token == "###############################################################################":
            # Toggle the in_header flag
            in_header = not in_header
        elif in_header:
            # Append the token with leading/trailing whitespace removed to the header array
            header.append(token.strip())

    return header

def main(input_file):
    content = read_input_file(input_file)
    tokens = tokenize(content)
    header = parse_tokens(tokens)
    print(header)
    return tokens

if __name__ == '__main__':
    input_file = os.path.join('path', 'to', 'input_file.mm')
    main(input_file)
