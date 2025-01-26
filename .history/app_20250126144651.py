from flask import Flask, request, jsonify, render_template_string
import os
import cv2
import pytesseract
import pandas as pd
import datetime
import subprocess

app = Flask(__name__)

# Global variable to store OCR processed data
processed_data = []

@app.route('/')
def index():
    # Check if Tesseract is installed and in the PATH
    try:
        tesseract_version = subprocess.check_output(["tesseract", "--version"])
    except Exception as e:
        return f"Tesseract not found: {e}", 500

    return render_template_string("""
        <!doctype html>
        <title>OCR Processing Service</title>
        <h1>OCR Processing Service</h1>
        <form action="/process" method="post" enctype="multipart/form-data">
            <input type="submit" value="Process Images">
        </form>
        {% if processed_data %}
            <h2>Processed Text:</h2>
            <ul>
                {% for item in processed_data %}
                    <li><strong>{{ item['filename'] }}:</strong> {{ item['text'] }}</li>
                {% endfor %}
            </ul>
        {% endif %}
        <pre>{{ tesseract_version.decode("utf-8") }}</pre>
    """, processed_data=processed_data, tesseract_version=tesseract_version)

@app.route('/process', methods=['POST'])
def process_images():
    global processed_data
    folder_path = 'Fotos'
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'output_{timestamp}.csv'
    data = []

    # Check if the folder exists
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Fotos directory does not exist.'}), 404

    # Check if the folder is empty
    if not os.listdir(folder_path):
        return jsonify({'error': 'Fotos directory is empty.'}), 404

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            try:
                img = cv2.imread(img_path)
                if img is None:
                    return jsonify({'error': f'Failed to read image {filename}'}), 400
                text = pytesseract.image_to_string(img)
                data.append({'filename': filename, 'text': text})
            except Exception as e:
                return jsonify({'error': f'Error processing image {filename}: {str(e)}'}), 500

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    # Update the global variable with the processed data
    processed_data = data

    return jsonify({'message': 'Processing complete', 'output_file': output_file})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)