from flask import Flask, request, jsonify, send_file, render_template
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Save the uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Remove the background
        input_image = Image.open(input_path)
        output_image = remove(input_image)

        # Save the output image in PNG format
        output_filename = os.path.splitext(file.filename)[0] + '.png'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        output_image.save(output_path, format="PNG")

        return jsonify({'filename': output_filename})

@app.route('/download/<filename>', methods=['GET'])
def download_image(filename):
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)