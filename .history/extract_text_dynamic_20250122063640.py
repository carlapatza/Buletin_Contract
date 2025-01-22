import os
from PIL import Image
import pytesseract

# Set the Tesseract command path from environment variables
tesseract_path = os.environ.get('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Path to the folder containing JPEG files
folder_path = 'foto'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # Construct full file path
        file_path = os.path.join(folder_path, filename)
        
        # Open the image file
        img = Image.open(file_path)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        
        # Print the extracted text
        print(f'Text from {filename}:\n{text}\n')
