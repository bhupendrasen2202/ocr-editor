from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            if filename.lower().endswith('.pdf'):
                images = convert_from_path(file_path)
                for img in images:
                    extracted_text += pytesseract.image_to_string(img)
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(image)

    return render_template('index.html', extracted_text=extracted_text)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)