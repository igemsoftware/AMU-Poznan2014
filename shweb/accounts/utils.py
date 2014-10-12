import random
from string import digits, ascii_letters as letters


def code_generator():
    code = [random.choice(digits+letters+'_-') for x in range(40)]
    return ''.join(code)
