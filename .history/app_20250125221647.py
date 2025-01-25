from flask import Flask, request, jsonify
import os
import cv2
import pytesseract
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the OCR Flask App!"

@app.route('/process', methods=['POST'])
def process_images():
    folder_path = 'Fotos'
    output_file = 'output.csv'
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            text = pytesseract.image_to_string(img)
            data.append({'filename': filename, 'text': text})

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    return jsonify({'message': 'Processing complete', 'output_file': output_file})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```
# Requirements
Flask
opencv-python
pytesseract
pandas