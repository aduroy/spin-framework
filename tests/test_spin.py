'''
@author: Antonin Duroy
'''
import unittest
from spin import Spin

class Test(unittest.TestCase):


    def test_unspin(self):
        masterspin = 'Result: {a|{b|c}} {{d|e}|f}'
        spuns = ['Result: a d',
                 'Result: a e',
                 'Result: a f',
                 'Result: b d',
                 'Result: b e',
                 'Result: b f',
                 'Result: c d',
                 'Result: c e',
                 'Result: c f']
        
        spin = Spin(masterspin)
        self.assertTrue(spin.unspin() in spuns)


if __name__ == "__main__":
    unittest.main()