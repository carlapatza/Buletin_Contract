from flask import Flask, jsonify, request
import psycopg2
import pytesseract
from PIL import Image
import os
from config import DATABASE_CONFIG

app = Flask(__name__)


def get_db_connection():  
    # Database connection
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn


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

    # Logic to insert the extracted data into the database
    conn = get_db_connection()
    cur = conn.cursor()
    # Assuming the ID data is structured; you may need to parse it accordingly
    cur.execute("INSERT INTO your_table_name (column_name) VALUES (%s)", (id_data,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Data uploaded successfully!"})


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
    app.run(debug=True)
