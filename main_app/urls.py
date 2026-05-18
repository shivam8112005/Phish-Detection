from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('url-detection/', views.url_detection_view, name='url_detection'),
    path('email-detection/', views.email_detection_view, name='email_detection'),
    path('sms-detection/', views.sms_detection_view, name='sms_detection'),
    path('file-analysis/', views.file_analysis_view, name='file_analysis'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
] 