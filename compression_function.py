from rounds_16_preprocessing import Splitting
from shift_function import s
import math

class Compression:
    def __init__(self, text, binary_encoded_list):
        self.text = text
        self.binary_encoded_list = binary_encoded_list
        
        # MD5 Initial Hash Values 
        self.register_bit = {
            'a': 0x67452301,
            'b': 0xEFCDAB89,
            'c': 0x98BADCFE,
            'd': 0x10325476
        }
        
        # K constant 
        self.k = [int(abs(2**32 * abs(math.sin(i + 1)))) & 0xFFFFFFFF for i in range(64)]
        
        splitting = Splitting(text, binary_encoded_list)
        self.first_32_bit_list, self.final_32_bit_list = splitting.break_padding_sequence()
    
    def f_function(self, x, y, z):
        return (x & y) | (~x & z)
    
    def g_function(self, x, y, z):
        return (x & z) | (y & ~z)
    
    def h_function(self, x, y, z):
        return x ^ y ^ z
    
    def i_function(self, x, y, z):
        return y ^ (x | ~z)
    
    def left_rotate(self, x, amount):
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF
    
    def md5_step(self):
        all_blocks = self.first_32_bit_list if len(self.final_32_bit_list) == 0 else self.first_32_bit_list + [self.final_32_bit_list]

        for block in all_blocks:  #  each 512-bit block
            A, B, C, D = int(str(self.register_bit['a']), 16), int(str(self.register_bit['b']), 16), int(str(self.register_bit['c']), 16), int(str(self.register_bit['d']), 16)

            for i in range(64):
                if i <= 15:
                    f = (B & C) | (~B & D)
                    g = i
                elif i <= 31:
                    f = (B & D) | (C & ~D)
                    g = (5 * i + 1) % 16
                elif i <= 47:
                    f = B ^ C ^ D
                    g = (3 * i + 5) % 16
                else:
                    f = C ^ (B | ~D)
                    g = (7 * i) % 16

                int_bin = int("".join(str(element) for element in block[g]),2)
                f = (f + A + int_bin + int(str(self.k[i]), 16)) & 0xFFFFFFFF
                A, D, C, B = D, C, B, (B + self.left_rotate(f, s[i])) & 0xFFFFFFFF  #  circular shift

        # Update hash values
            self.register_bit['a'] = (int(str(self.register_bit['a']), 16) + A) & 0xFFFFFFFF
            self.register_bit['b'] = (int(str(self.register_bit['b']), 16) + B) & 0xFFFFFFFF
            self.register_bit['c'] = (int(str(self.register_bit['c']), 16) + C) & 0xFFFFFFFF
            self.register_bit['d'] = (int(str(self.register_bit['d']), 16) + D) & 0xFFFFFFFF

        def little_endian(val):
            return ''.join(format(val, '08x')[i:i+2] for i in range(6, -1, -2))

        md5_hash = ''.join(little_endian(self.register_bit[key]) for key in ['a', 'b', 'c', 'd'])

        print(f"Final MD5 Hash: {md5_hash}")
        return md5_hash

                   

