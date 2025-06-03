from flask import Flask, render_template, request, send_file
import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    ocr_text = ""

    if filename.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        for img in images:
            ocr_text += pytesseract.image_to_string(img) + "\n"
    else:
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img)

    return {"text": ocr_text}

@app.route("/save", methods=["POST"])
def save():
    content = request.form["content"]
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    lines = content.splitlines()
    y = height - 40
    for line in lines:
        p.drawString(40, y, line)
        y -= 15
        if y < 40:
            p.showPage()
            y = height - 40
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="edited_output.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
