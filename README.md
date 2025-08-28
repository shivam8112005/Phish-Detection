# CyberGuard - Django Security Platform

A comprehensive cybersecurity platform built with Django that provides AI-powered threat detection for URLs, emails, SMS messages, and documents.

## Features

### 🔒 Security Detection
- **URL Analysis**: Detect phishing sites and malicious URLs
- **Email Security**: Identify spam and phishing emails
- **SMS Detection**: Analyze SMS messages for smishing attacks
- **Document Security**: Scan PDF and text files for threats

### 👤 User Management
- User registration and authentication
- Personal dashboard with security statistics
- Profile management with additional details
- Activity tracking and history

### 🤖 AI-Powered Chatbot
- Built-in security assistant
- Real-time threat analysis
- Security tips and guidance
- Powered by Google Gemini AI

### 📊 Analytics & Tracking
- Detection result history
- User activity logging
- Security statistics
- Confidence scoring

## Technology Stack

- **Backend**: Django 5.0.2
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **AI/ML**: Google Gemini AI, Custom ML models
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom cybersecurity theme
- **File Processing**: PyPDF2 for PDF analysis

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cyberguard-django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   google_api_key=your_google_gemini_api_key_here
   SECRET_KEY=your_django_secret_key_here
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
cyberguard_django/
├── cyberguard_django/          # Main project settings
├── main_app/                   # Core application
│   ├── models.py              # Detection and activity models
│   ├── views.py               # Main views and detection logic
│   ├── forms.py               # Detection forms
│   ├── urls.py                # URL routing
│   └── admin.py               # Admin configuration
├── user_auth/                 # User authentication app
│   ├── models.py              # User profile model
│   ├── views.py               # Auth views
│   ├── forms.py               # User forms
│   ├── urls.py                # Auth URL routing
│   └── admin.py               # User admin
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── main_app/             # Main app templates
│   └── user_auth/            # Auth templates
├── static/                    # Static files
│   └── css/
│       └── style.css         # Main stylesheet
├── media/                     # User uploaded files
├── requirements.txt           # Python dependencies
└── manage.py                 # Django management script
```

## Usage

### For Users

1. **Register/Login**: Create an account or sign in
2. **Dashboard**: View your security statistics and recent activity
3. **Security Tools**:
   - **URL Detection**: Paste suspicious URLs for analysis
   - **Email Security**: Analyze email content for threats
   - **SMS Detection**: Check SMS messages for smishing
   - **File Analysis**: Upload PDF/TXT files for scanning
4. **Chatbot**: Use the security assistant for guidance

### For Administrators

1. **Admin Panel**: Access at `/admin`
2. **User Management**: Monitor user accounts and activities
3. **Detection Results**: View all security scans and results
4. **Analytics**: Track system usage and threat patterns

## API Endpoints

- `GET /` - Home page
- `GET /url-detection/` - URL analysis page
- `GET /email-detection/` - Email analysis page
- `GET /sms-detection/` - SMS analysis page
- `GET /file-analysis/` - File analysis page
- `GET /about/` - About page
- `GET /contact/` - Contact page
- `POST /chatbot/` - AI chatbot API
- `GET /auth/signup/` - User registration
- `GET /auth/login/` - User login
- `GET /auth/profile/` - User profile
- `GET /auth/dashboard/` - User dashboard

## Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Secure login/logout system
- **File Upload Security**: Validated file types and sizes
- **Input Validation**: All user inputs are validated
- **Activity Logging**: Track user activities for security
- **Secure Headers**: Django security middleware enabled

## Customization

### Styling
- Modify `static/css/style.css` for theme changes
- Update color variables in CSS root for branding

### Models
- Extend `DetectionResult` model for additional detection types
- Add fields to `UserProfile` for more user information

### Views
- Customize detection logic in `main_app/views.py`
- Add new security features as needed

## Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Use HTTPS in production

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with Django deployment
- **AWS**: EC2 with RDS database
- **Google Cloud**: App Engine or Compute Engine

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: security@cyberguard.com
- Documentation: Check the admin panel for detailed guides
- Issues: Use the GitHub issues page

## Acknowledgments

- Google Gemini AI for chatbot functionality
- Django community for the excellent framework
- Cybersecurity community for threat intelligence 