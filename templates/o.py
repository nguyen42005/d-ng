from flask import Flask, render_template, request, send_file, redirect, url_for
from Crypto.Cipher import DES
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

KEY_SIZE = 8

# Padding
pad = lambda s: s + b" " * (8 - len(s) % 8)
unpad = lambda s: s.rstrip(b" ")

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    des = DES.new(key, DES.MODE_ECB)
    encrypted_data = des.encrypt(pad(data))``
    output_path = file_path + '.enc'
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)
    return output_path

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    des = DES.new(key, DES.MODE_ECB)
    decrypted_data = unpad(des.decrypt(data))
    output_path = file_path.replace('.enc', '.dec')
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    key = request.form['key'].encode()
    uploaded_file = request.files['file']

    if len(key) != KEY_SIZE:
        return 'Key must be exactly 8 bytes (8 characters).'

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        if action == 'encrypt':
            result_path = encrypt_file(file_path, key)
        else:
            result_path = decrypt_file(file_path, key)

        return send_file(result_path, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
