import unittest
import ias_functions
import memoria as mem
from numpy import binary_repr
from bitstring import BitStream

class test(unittest.TestCase):

    def test_memoria(self):
        
        l = [0,0,0]
        
        a = binary_repr(1,40)[1:41]
        
        #self.assertEqual(BitStream(bin = '0b'+ '1000001').int, -1, 'Os números são iguais')
        self.assertEqual(l [int('000010',2)], 0, msg= 'Está correto')
        self.assertEqual(len(BitStream(bin = 1, length = 40).bin), 40)


if __name__ == '__main__':
    unittest.main()