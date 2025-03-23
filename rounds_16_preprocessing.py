from text_to_padding import Padding
import sys
sys.set_int_max_str_digits(10000)
class Splitting:
    def __init__(self,text,binary_encoded_list):
        self.text = text
        self.binary_encoded_list = binary_encoded_list
        self.length_check = len(binary_encoded_list)
        padding = Padding(text,binary_encoded_list)
        self.first_block,self.final_block=padding.binary_to_padding()
        self.first_64_bit_list = []
        self.final_64_bit_list = []
    
    def break_padding_sequence(self):  # 1024 ---> 64 bits , (16 ,0-15) + (15-79) 
        
        if self.length_check < 448:
            for i in range(0,len(self.first_block),32):
                self.first_64_bit_list.append(self.first_block[i:i+32])
            return self.first_64_bit_list
        
        elif 448 < self.length_check < 512:
            for i in range(0,len(self.first_block),32):     # first block 
                self.first_64_bit_list.append(self.first_block[i:i+32])
            
            for j in range(0,len(self.final_block),32):      # final block
                self.final_64_bit_list.append(self.final_block[j:j+32])
           
            
            return self.first_64_bit_list , self.final_64_bit_list
        
        elif self.length_check % 512 == 0:
            num_blocks = self.length_check // 512
            first_blocks = [self.binary_encoded_list[i*512 :(i+1) * 512] for i in range(num_blocks)]
            for block in first_blocks:
                block_list = [block[j:j+32] for j in range(0,512,32)]
                self.first_64_bit_list.append(block_list)
           
            for j in range(0,len(self.final_block),32):
                self.final_64_bit_list.append(self.final_block[j:j+32])
            
            return self.first_64_bit_list , self.final_64_bit_list
        
        else:
            num_blocks = self.length_check // 512
            first_blocks = [self.binary_encoded_list[i * 512 : (i+1) * 512] for i in range(num_blocks)]
            for block in first_blocks:
                block_list = [block[j:j+32] for j in range(0,512,32)]
                self.first_64_bit_list.append(block_list)
            
            for j in range(0,len(self.final_block),32):
                self.final_64_bit_list.append(self.final_block[j:j+32])
           
            return self.first_64_bit_list , self.final_64_bit_list

