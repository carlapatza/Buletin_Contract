from flask import Flask, jsonify, request
import pytesseract
from PIL import Image
import os


app = Flask(__name__)


@app.route('/upload_id', methods=['POST'])  
def upload_id():
    # Get the image file from the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read the image and extract text
    image = Image.open(file)
    id_data = pytesseract.image_to_string(image)

    # Return the extracted text
    return jsonify({"extracted_text": id_data})


@app.route('/process_ids', methods=['GET'])
def process_ids():
    folder_path = 'foto'
    results = []  # Initialize results list

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            id_data = pytesseract.image_to_string(image)
            results.append({"filename": filename, "data": id_data})

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=int(os.environ.get('PORT', 8080)), 
            debug=False)
