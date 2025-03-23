class Padding:
    def __init__(self,text,binary_encoded_list):
        self.text = text
        self.reversed_rem_list = binary_encoded_list
    
    def one_two_eight_bit_add(self,text):
        bits_list = []  
        reversed_bits_list = []
        zero_list = []
        bits_value = len(text) * 8 
        while bits_value != 0:
            rem = bits_value % 2
            bits_list.append(rem)
            bits_value = bits_value // 2
        for i in range(len(bits_list)-1,-1,-1):
            reversed_bits_list.append(bits_list[i])
        zero_add_length = 64 - len(reversed_bits_list)
        for _ in range(zero_add_length):
            zero_list.append(0)
        concatenate_list = zero_list + reversed_bits_list 
        return concatenate_list

    def binary_to_padding(self):

        if len(self.reversed_rem_list) < 512:
            if len(self.reversed_rem_list) < 448:
                self.reversed_rem_list.append(1)
                plain_text_length = len(self.reversed_rem_list)
                zero_add_length = 448 - plain_text_length
                for _ in range(zero_add_length):                      
                    self.reversed_rem_list.append(0)
                one_two_eight_bit_list = self.one_two_eight_bit_add(self.text) 
                first_block = self.reversed_rem_list + one_two_eight_bit_list
                return first_block,None
            else:
                first_block = []
                second_block = []
                # 1st block will contain 1024 - len(list) ----> 0
                self.reversed_rem_list.append(1)
                zero_add_length = 512 - len(self.reversed_rem_list)
                for _ in range(zero_add_length):
                    self.reversed_rem_list.append(0)
                first_block = self.reversed_rem_list
                # 2nd block this is a new block 896 zeros + 128 padded bits 
                for _ in range(448):
                    second_block.append(0)
                one_two_eight_bit_list = self.one_two_eight_bit_add(self.text)
                final_block = second_block + one_two_eight_bit_list
                return first_block,final_block
        else:
            if len(self.reversed_rem_list) % 512 == 0:
                first_block = []
                second_block = []
                # 1st block  1024 bits binary encoded number
                for i in range(0,len(self.reversed_rem_list),512):
                    first_block.append(self.reversed_rem_list[i: 512 + i])
                # 2nd block  --> 896 zero + 128 bits
                second_block.append(1)
                zero_add_length = 448 - len(second_block)
                for _ in range(zero_add_length):
                    second_block.append(0)
                one_two_eight_bit_list = self.one_two_eight_bit_add(self.text)
                final_block = second_block + one_two_eight_bit_list
                return first_block,final_block
            else:
                first_block = []
                second_block = []
                # 1st block ---> contain 1024,1024,remaining length
                num_blocks = len(self.reversed_rem_list) // 512
                for i in range(0,len(self.reversed_rem_list),512):
                    first_block.append(self.reversed_rem_list[i:512+i])
                # 2nd block ---> padd remaining length 
                second_block = first_block[num_blocks]
                second_block.append(1)
                zero_add_length = 448 - len(second_block)
                for _ in range(zero_add_length):
                    second_block.append(0)
                one_two_eight_bit_list = self.one_two_eight_bit_add(self.text)
                final_block = second_block + one_two_eight_bit_list
                return [first_block[i] for i in range(num_blocks)],final_block

