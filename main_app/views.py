from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json
import pickle
import os
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import google.generativeai as genai
from dotenv import load_dotenv
import time
import requests

from .forms import URLDetectionForm, EmailDetectionForm, SMSDetectionForm, FileAnalysisForm
from .models import DetectionResult, UserActivity

load_dotenv()


HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")




API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
     "Content-Type": "application/json"
}



def load_models():
    try:
        sms_model_path = 'sms_pipeline.pkl'
        email_model_path = 'email_pipeline.pkl'
        url_model_path = 'url_pipeline (1).pkl'
        
        with open(sms_model_path, 'rb') as file:
            sms_model = pickle.load(file)
        
        with open(email_model_path, 'rb') as file:
            email_model = pickle.load(file)
        
        with open(url_model_path, 'rb') as file:
            url_model = pickle.load(file)
        
        return sms_model, email_model, url_model
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None, None

sms_model, email_model, url_model = load_models()

def home_view(request):
    return render(request, 'main_app/index.html')

def about_view(request):
    return render(request, 'main_app/about.html')

def contact_view(request):
    return render(request, 'main_app/contact.html')

def url_detection_view(request):
    if request.method == 'POST':
        form = URLDetectionForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            if url_model:
                proba = url_model.predict_proba([url])[0]
                threshold = 0.4
                prediction = 1 if proba[1] >= threshold else 0
                result = "Phishing" if prediction == 1 else "Legitimate"
                confidence = max(proba)
            else:
                result = "Model not available"
                confidence = 0.0
            
            if request.user.is_authenticated:
                DetectionResult.objects.create(
                    user=request.user,
                    detection_type='url',
                    input_data=url,
                    result='dangerous' if result == "Phishing" else 'safe',
                    confidence_score=confidence
                )
            
            return render(request, 'main_app/url_detection.html', {
                'form': form,
                'url_result': result,
                'url_entered': url,
                'confidence': f"{confidence:.2%}"
            })
    else:
        form = URLDetectionForm()
    
    return render(request, 'main_app/url_detection.html', {'form': form})

def email_detection_view(request):
    if request.method == 'POST':
        form = EmailDetectionForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            
            email_text = f"{subject} {content} {sender}"
            
            if email_model:
                proba = email_model.predict_proba([email_text])[0]
                threshold = 0.4
                prediction = 1 if proba[1] >= threshold else 0
                result = "Spam" if prediction == 1 else "Legitimate"
                confidence = max(proba)
            else:
                result = "Model not available"
                confidence = 0.0
            
            if request.user.is_authenticated:
                DetectionResult.objects.create(
                    user=request.user,
                    detection_type='email',
                    input_data=email_text,
                    result='dangerous' if result == "Spam" else 'safe',
                    confidence_score=confidence
                )
            
            return render(request, 'main_app/email_detection.html', {
                'form': form,
                'email_result': result,
                'email_data': {
                    'sender': sender,
                    'subject': subject,
                    'content': content
                },
                'confidence': f"{confidence:.2%}"
            })
    else:
        form = EmailDetectionForm()
    
    return render(request, 'main_app/email_detection.html', {'form': form})

def sms_detection_view(request):
    if request.method == 'POST':
        form = SMSDetectionForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            
            transformed_text = transform_text(message)
            
            if sms_model:
                proba = sms_model.predict_proba([transformed_text])[0]
                threshold = 0.4
                prediction = 1 if proba[1] >= threshold else 0
                result = "Spam" if prediction == 1 else "Legitimate"
                confidence = max(proba)
            else:
                result = "Model not available"
                confidence = 0.0
            
            if request.user.is_authenticated:
                DetectionResult.objects.create(
                    user=request.user,
                    detection_type='sms',
                    input_data=message,
                    result='dangerous' if result == "Spam" else 'safe',
                    confidence_score=confidence
                )
            
            return render(request, 'main_app/sms_detection.html', {
                'form': form,
                'sms_result': result,
                'sms_message': message,
                'confidence': f"{confidence:.2%}"
            })
    else:
        form = SMSDetectionForm()
    
    return render(request, 'main_app/sms_detection.html', {'form': form})

def file_analysis_view(request):
    if request.method == 'POST':
        form = FileAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            extracted_text = ""
            if file.name.endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                except Exception as e:
                    messages.error(request, 'Error reading PDF file.')
                    return render(request, 'main_app/file_analysis.html', {'form': form})
            elif file.name.endswith('.txt'):
                try:
                    extracted_text = file.read().decode('utf-8')
                except Exception as e:
                    messages.error(request, 'Error reading text file.')
                    return render(request, 'main_app/file_analysis.html', {'form': form})
            
            if not extracted_text.strip():
                messages.error(request, 'File is empty or could not extract text.')
                return render(request, 'main_app/file_analysis.html', {'form': form})
            
            if email_model:
                proba = email_model.predict_proba([extracted_text])[0]
                threshold = 0.4
                prediction = 1 if proba[1] >= threshold else 0
                result = "Spam" if prediction == 1 else "Legitimate"
                confidence = max(proba)
            else:
                result = "Model not available"
                confidence = 0.0
            
            if request.user.is_authenticated:
                DetectionResult.objects.create(
                    user=request.user,
                    detection_type='file',
                    input_data=extracted_text[:500],
                    result='dangerous' if result == "Spam" else 'safe',
                    confidence_score=confidence
                )
            
            return render(request, 'main_app/file_analysis.html', {
                'form': form,
                'message': result,
                'confidence': f"{confidence:.2%}"
            })
    else:
        form = FileAnalysisForm()
    
    return render(request, 'main_app/file_analysis.html', {'form': form})

def transform_text(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
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

def call_gemini(model, prompt):     
    retries = 5
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Error: {e}")

        wait_time = 2 * attempt
        print(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

    return "Sorry, I couldn't process your request."





def call_hf_chat(messages):
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita",
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 500
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    data = response.json()

    if "error" in data:
        return f"HF Error: {data['error']}"

    return data["choices"][0]["message"]["content"]

chat_history = []

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_view(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"response": "Please enter a message."})
        
        chat_history.append({"role": "user", "content": user_message})

        system_prompt = """
            You are CyberGuard, a cybersecurity assistant chatbot.

            RULES:
            - Respond ONLY to the user's latest message
            - Do NOT continue or simulate conversations
            - Do NOT add roles like USER or CYBERGUARD
            - Do NOT generate multi-turn dialogues
            - Give a single, direct answer only
            - Keep responses short and clear
            """
        messages = [{"role": "system", "content": system_prompt}] + chat_history

        response_text = call_hf_chat(messages)

        chat_history.append({"role": "assistant", "content": response_text})

        return JsonResponse({"response": response_text})

    except Exception as e:
        return JsonResponse({"response": f"Error: {str(e)}"})
