from flask import Flask, jsonify
import psycopg2
from config import DATABASE_CONFIG

app = Flask(__name__)

def get_db_connection():
    # Database connection
    conn = psycopg2.connect(**DATABASE_CONFIG)

    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn


@app.route('/upload_id', methods=['POST'])  

def upload_id():
    # Logic to read data from ID card and store in database
    return jsonify({"message": "Data uploaded successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
