# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# import os
# import PyPDF2
# from dotenv import load_dotenv
# import pickle

# load_dotenv()

# # Load models
# sms_model_path = 'sms_pipeline.pkl'
# email_model_path = 'email_pipeline.pkl'
# url_model_path = 'url_pipeline (1).pkl'

# with open(sms_model_path, 'rb') as file:
#     sms_model = pickle.load(file)

# with open(email_model_path, 'rb') as file:
#     email_model = pickle.load(file)

# with open(url_model_path, 'rb') as file:
#     url_model = pickle.load(file)

# api_key = os.getenv("google_api_key")

# # Flask app
# app = Flask(__name__)

# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scam/', methods=['GET', 'POST'])
# def detect_scam():
#     if "file" not in request.files:
#         return render_template('index.html', message="Please Upload a File!")
    
#     file = request.files['file']
#     print(file)
    
#     extracted_text = ""
#     if file.filename.endswith('.pdf'):
#         pdf_reader = PyPDF2.PdfReader(file)
#         extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
#     elif file.filename.endswith('.txt'):
#         extracted_text = file.read().decode('utf-8')
#     else:
#         return render_template('index.html', message='Error fetching the text! File is Empty or please Enter .pdf or .txt file only.')
    
#     print(extracted_text)
#     return render_template('index.html', message="File analyzed successfully!")

# @app.route("/url_predict", methods=["POST"])
# def url_predict():
#     if request.method == "POST":
#         url = request.form["url"]
        
#         # Predict using the URL model
#         proba = url_model.predict_proba([url])[0]
#         threshold = 0.4  # make model more sensitive to phishing
#         prediction = 1 if proba[1] >= threshold else 0
        
#         print("Prediction:", prediction)
#         print("Probability:", proba)
        
#         result = "Phishing" if prediction == 1 else "Legitimate"
#         return render_template("index.html", url_result=result, url_entered=url)

# @app.route("/email_predict", methods=["POST"])
# def email_predict():
#     if request.method == "POST":
#         subject = request.form["subject"]
#         content = request.form["content"]
#         sender = request.form["sender"]
        
#         # Combine email data for prediction
#         email_text = f"{subject} {content} {sender}"
        
#         # Predict using the email model
#         proba = email_model.predict_proba([email_text])[0]
#         threshold = 0.5
#         prediction = 1 if proba[1] >= threshold else 0
        
#         result = "Spam" if prediction == 1 else "Legitimate"
#         return render_template("index.html", email_result=result, email_data={
#             'subject': subject,
#             'content': content,
#             'sender': sender
#         })

# @app.route("/sms_predict", methods=["POST"])
# def sms_predict():
#     if request.method == "POST":
#         message = request.form["message"]
        
#         # Predict using the SMS model
#         proba = sms_model.predict_proba([message])[0]
#         threshold = 0.5
#         prediction = 1 if proba[1] >= threshold else 0
        
#         result = "Spam" if prediction == 1 else "Legitimate"
#         return render_template("index.html", sms_result=result, sms_message=message)

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import PyPDF2
from dotenv import load_dotenv
import pickle

load_dotenv()

# Load models
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

# Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/url-detection')
def url_detection():
    return render_template('url_detection.html')

@app.route('/email-detection')
def email_detection():
    return render_template('email_detection.html')

@app.route('/sms-detection')
def sms_detection():
    return render_template('sms_detection.html')

@app.route('/file-analysis')
def file_analysis():
    return render_template('file_analysis.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/scam/', methods=['GET', 'POST'])
def detect_scam():
    if "file" not in request.files:
        return render_template('file_analysis.html', message="Please Upload a File!")
    
    file = request.files['file']
    print(file)
    
    extracted_text = ""
    if file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif file.filename.endswith('.txt'):
        extracted_text = file.read().decode('utf-8')
    else:
        return render_template('file_analysis.html', message='Error fetching the text! File is Empty or please Enter .pdf or .txt file only.')
    
    print(extracted_text)
    return render_template('file_analysis.html', message="File analyzed successfully!")

@app.route("/url_predict", methods=["POST"])
def url_predict():
    if request.method == "POST":
        url = request.form["url"]
        
        # Predict using the URL model
        proba = url_model.predict_proba([url])[0]
        threshold = 0.4  # make model more sensitive to phishing
        prediction = 1 if proba[1] >= threshold else 0
        
        print("Prediction:", prediction)
        print("Probability:", proba)
        
        result = "Phishing" if prediction == 1 else "Legitimate"
        return render_template("url_detection.html", url_result=result, url_entered=url)

@app.route("/email_predict", methods=["POST"])
def email_predict():
    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]
        sender = request.form["sender"]
        
        # Combine email data for prediction
        email_text = f"{subject} {content} {sender}"
        
        # Predict using the email model
        proba = email_model.predict_proba([email_text])[0]
        threshold = 0.4
        prediction = 1 if proba[1] >= threshold else 0
        
        result = "Spam" if prediction == 1 else "Legitimate"
        return render_template("email_detection.html", email_result=result, email_data={
            'subject': subject,
            'content': content,
            'sender': sender
        })

@app.route("/sms_predict", methods=["POST"])
def sms_predict():
    if request.method == "POST":
        message = request.form["message"]
        
        # Predict using the SMS model
        proba = sms_model.predict_proba([message])[0]
        threshold = 0.5
        prediction = 1 if proba[1] >= threshold else 0
        
        result = "Spam" if prediction == 1 else "Legitimate"
        return render_template("sms_detection.html", sms_result=result, sms_message=message)

if __name__ == '__main__':
    app.run(debug=True)

