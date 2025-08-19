from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import PyPDF2
from dotenv import load_dotenv
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import time


load_dotenv()
api_key = os.getenv("google_api_key")


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
    

def transform_text(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    # print(text)
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
    return " ".join(y).strip()

@app.route("/sms_predict", methods=["POST"])
def sms_predict():
    if request.method == "POST":
        message = request.form["message"]
        
        # Predict using the SMS model
        transformed_text = transform_text(message)
        proba = sms_model.predict_proba([transformed_text])[0]
        threshold = 0.4
        prediction = 1 if proba[1] >= threshold else 0
        
        result = "Spam" if prediction == 1 else "Legitimate"
        return render_template("sms_detection.html", sms_result=result, sms_message=message)
    




def call_gemini(model, prompt):
    retries = 5
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            if response and response.text:  
                 # valid response
                print("bot response: ",response)
                return response.text
            print("outside if")
        except Exception as e:
            print(f"Error: {e}")

        # wait before retry
        wait_time = 2 * attempt  
        print(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

    return "Sorry, I couldn’t process your request."




@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            generation_config={
                "temperature": 0.4,
                "top_p": 1,
                "top_k": 32,
                "max_output_tokens": 4096
            }
        )

        # System instruction (make it cybersecurity focused)
        system_prompt = """Name: 🛡️ CyberGuard

Role:
You are CyberGuard, a friendly and knowledgeable cybersecurity assistant chatbot.
Your job is to help everyday users understand online threats such as phishing, scams, malware, spam messages, and suspicious links.

Guidelines:

Always explain threats in simple, non-technical language.

Give practical safety tips that users can easily follow.

Stay calm, reassuring, and supportive, never alarming.

Provide examples when possible (e.g., fake messages, scam email tricks).

Do not use jargon unless absolutely necessary—and if used, explain it in plain words.

Encourage users to double-check links, update software, and use strong passwords.

Do not give hacking instructions, malware creation tips, or anything harmful.

Capabilities:

Detect signs of phishing/scam in text or links provided by the user.

Explain risks of malware attachments or shady websites.

Educate users about safe browsing, email hygiene, and password best practices.

Help them identify when to report a scam or delete suspicious content.

"""

        response = model.generate_content([system_prompt, user_message])
        response_call_gemini = call_gemini(model, user_message)
        
        return jsonify({"response": response_call_gemini})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})





if __name__ == '__main__':
    app.run(debug=True)

