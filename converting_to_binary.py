def convert_text_to_binary(text):
    binary_encoded_list = []  # This will store the binary encoding of a text
    for char in text:
        number = ord(char)
        rem_list = [] 
        while number != 0:
            rem_list.append(number % 2)
            number = number // 2
        rem_list.reverse()  
        binary_encoded_list.extend(rem_list)  
    return binary_encoded_list

