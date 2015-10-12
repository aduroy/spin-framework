'''
@author: Antonin Duroy
'''

import re
import random

class Spin():
    
    def __init__(self, masterspin=None, input_file=None):
        if masterspin is not None:
            self.masterspin = masterspin
        elif input_file is not None:
            self.masterspin = self.__open_file(input_file)
        else:
            raise ValueError("A masterspin must be specified.")
    
    def unspin(self, delimiter='|'):
        spun_string = self.masterspin
        while True:
            spun_string, n = re.subn('{([^{}]*)}',
                lambda m: random.choice(m.group(1).split(delimiter)),
                spun_string)
            if n == 0:
                break
        return spun_string.strip()
    
    def __open_file(self, path):
        with open(path, "r") as masterspin:
            return masterspin.read()