"""
.. module:: shweb.accounts
   :platform: Unix, Windows
   :synopsis: Module with utils for accounts application.

"""

import random
from string import digits, ascii_letters as letters


def code_generator(length=40):
    """Function for generating random string with given length

    Args:
        length: length of the random string

    Returns:
        str object
    """
    code = [random.choice(digits+letters+'_-') for x in range(length)]
    return ''.join(code)
