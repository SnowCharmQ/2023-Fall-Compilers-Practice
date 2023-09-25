import re
import logging
import argparse

transition_diagram = {
    'start': {
        'letter': 'identifier',
        'digit': 'number',
        'simple_op': 'simple_op',
        'complex_op': 'complex_op',
        'space': 'start',
        'neg': 'neg'
    },
    'identifier': {
        'letter': 'identifier',
        'digit': 'identifier',
        'simple_op': 'retract',
        'complex_op': 'retract',
        'space': 'start',
        'neg': 'retract'
    },
    'number': {
        'letter': 'error',
        'digit': 'number',
        'simple_op': 'retract',
        'complex_op': 'retract',
        'space': 'start',
        'neg': 'retract'
    },
    'simple_op': {
        'letter': 'retract',
        'digit': 'retract',
        'simple_op': 'error',
        'complex_op': 'error',
        'space': 'start',
        'neg': 'error'
    },
    'complex_op': {
        'letter': 'retract',
        'digit': 'retract',
        'simple_op': 'error',
        'complex_op': 'complex_op',
        'space': 'start',
        'neg': 'error'
    },
    'neg': {
        'letter': 'retract',
        'digit': 'number',
        'simple_op': 'error',
        'complex_op': 'error',
        'space': 'start',
        'neg': 'error'
    },
}

token_map = {
    'int': 'TYPE',
    'number': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RET',
    ';': 'SEMI',
    '=': 'ASSIGN',
    '<': 'LT',
    '<=': 'LE',
    '>': 'GT',
    '>=': 'GE',
    '!=': 'NE',
    '==': 'EQ',
    '+': 'PLUS',
    '-': 'MINUS',
    '(': 'LP',
    ')': 'RP',
    '{': 'LC',
    '}': 'RC',
    'error': 'ERROR'
}

simple_op = ['+', '(', ')', '{', '}', ';']
complex_op = ['=', '!', '<', '>']


def tokenize_code(code: str):
    tokens = []
    token = ''
    state = 'start'
    idx = 0
    while idx < len(code):
        char = code[idx]
        if char.isspace():
            char = 'space'
        elif char.isalpha() or char == '_' or char == '$':
            char = 'letter'
        elif char.isdigit():
            char = 'digit'
        elif char in simple_op:
            char = 'simple_op'
        elif char in complex_op:
            char = 'complex_op'
        elif char == '-':
            char = 'neg'
        else:
            char = 'error'
        state = transition_diagram[state].get(char, None)
        if state is not None:
            if state == 'retract':
                idx -= 1
                state = 'start'
            if state == 'start':
                if token:
                    logging.debug(f'Found token: {token}')
                    tokens.append(token)
                    token = ''
            elif state == 'error':
                tokens.append('error')
                break
            else:
                token += code[idx]
        else:
            tokens.append('error')
            logging.error(f'Error at {idx}')
            break
        idx += 1
    return tokens


def parse_tokens(tokens: list):
    outputs = []
    id_pattern = r'^[a-zA-Z_$][a-zA-Z0-9_$]*$'
    for token in tokens:
        output = token_map.get(token, None)
        if output is not None:
            outputs.append(output)
        elif re.match(id_pattern, token):
            outputs.append('ID')
        else:
            outputs.append('INT')
    return ' '.join(outputs).strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--code_path', help='root of code file to be analyzed', required=True)
    parser.add_argument('--ans_path', help='root of answer file to be compared')
    parser.add_argument('--test', help='test mode', action='store_true')
    parser.add_argument('--debug', help='debug mode', action='store_true')
    args = parser.parse_args()
    code_path = args.code_path
    ans_path = args.ans_path
    test = args.test
    debug = args.debug
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    with open(code_path, 'r') as f:
        code = f.read()
    tokens = tokenize_code(code)
    output = parse_tokens(tokens)
    if test:
        with open(ans_path, 'r') as f:
            ans = f.read()
        if output == ans:
            logging.info('Test passed')
            print(output)
        else:
            logging.error(f'{ans}')
            logging.error(f'{output}')
            logging.error('Test failed')
    else:
        print(output)
