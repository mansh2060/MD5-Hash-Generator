from flask import Flask, render_template, request
from text_to_padding import Padding
from compression_function import Compression

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    md5_hash = None
    if request.method == 'POST':
        text = request.form['text']
        binary_encoded_list = [int(bit) for bit in ''.join(format(ord(char), '08b') for char in text)]
        
        padding = Padding(text, binary_encoded_list)
        first_block, final_block = padding.binary_to_padding()
        
        compression = Compression(text, first_block if final_block is None else first_block + final_block)
        md5_hash = compression.md5_step()
    
    return render_template('index.html', md5_hash=md5_hash)

if __name__ == '__main__':
    app.run(debug=True)
