from flask import Flask, request, render_template, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign', methods=['POST'])
def sign_document():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = file.filename
        file_path = os.path.join('documents', filename)
        file.save(file_path)
        
        # Sign the document using OpenSSL with the USB token
        sign_command = f"openssl dgst -sha256 -sign engine:pkcs11 -keyform engine -engine pkcs11 -out documents/{filename}.sig {file_path}"
        subprocess.run(sign_command, shell=True, check=True)
        
        return send_file(f"documents/{filename}.sig", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)