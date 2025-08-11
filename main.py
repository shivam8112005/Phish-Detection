from flask import Flask, render_template, request
import google.generativeai as genai
import os
import PyPDF2


#app
app = Flask(__name__)

#routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scam/', methods = ['GET', 'POST'])
def detect_scam():
    if "file" not in request.files:
        return render_template('index.html', message="Please Upload a File !")
    file = request.files['file']
    print(file)
    extracted_text = ""

    if file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    elif file.filename.endswith('.txt'):
        extracted_text = file.read().decode('utf-8')
    else:
        return render_template('index.html', message='Error fetching the text! File is Empty or please Enter .pdf or .txt file only.')       

#python main
if  __name__ == '__main__':
    app.run(debug=True)