from flask import Flask, render_template, request
import google.generativeai as genai
import os
import PyPDF2
from dotenv import load_dotenv
import pickle

load_dotenv()


sms_model_path = 'sms_pipeline.pkl'
email_model_path = 'email_pipeline.pkl'
url_model_path = 'url_pipeline (1).pkl'
with open(sms_model_path, 'rb') as file:
    sms_model = pickle.load(file) 
with open(email_model_path, 'rb') as file:
    email_model = pickle.load(file) 
with open(url_model_path, 'rb') as file:
    url_model = pickle.load(file) 

api_key = os.getenv("google_api_key")
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
        extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    elif file.filename.endswith('.txt'):
        extracted_text = file.read().decode('utf-8')
    else:
        return render_template('index.html', message='Error fetching the text! File is Empty or please Enter .pdf or .txt file only.')  
    print(extracted_text)
    return render_template('index.html')




@app.route("/url_predict", methods=["POST"])
def url_predict():
    if request.method == "POST":
        url = request.form["url"]

        # ⚡ Here you need to transform the URL same way as you did in training
        # Example: simple feature (length of URL)
        # features = [[len(url)]]

        # Predict
        proba = url_model.predict_proba([url])[0]
        threshold = 0.4   # make model more sensitive to phishing
        prediction = 1 if proba[1] >= threshold else 0
        print("-------------------------------- ",prediction)
        print("-------------------------------- hjfbwiubwj f",proba)
        
        result = "Phishing" if prediction == 1 else "Legitimate"
        # print(result)

        return render_template("index.html", url_result=result, url_entered=url)




#python main
if  __name__ == '__main__':
    app.run(debug=True)