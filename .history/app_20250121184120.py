from flask import Flask, jsonify, request
import psycopg2
import pytesseract
from PIL import Image
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
cur.execute("INSERT INTO your_table_name (column_name) VALUES (%s)", (id_data,))  # Adjusted line length


    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Data uploaded successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
