from django import forms

class URLDetectionForm(forms.Form):
    url = forms.URLField(
        label='Enter URL to analyze',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com'
        })
    )

class EmailDetectionForm(forms.Form):
    sender = forms.EmailField(
        label='Sender Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'sender@example.com'
        })
    )
    subject = forms.CharField(
        label='Email Subject',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email subject line'
        })
    )
    content = forms.CharField(
        label='Email Content',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Paste the email content here...'
        })
    )

class SMSDetectionForm(forms.Form):
    message = forms.CharField(
        label='SMS Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Paste the SMS message here...'
        })
    )

class FileAnalysisForm(forms.Form):
    file = forms.FileField(
        label='Upload File',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.txt'
        }),
        help_text='Supported formats: PDF, TXT (Max size: 10MB)'
    )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 10MB.')
            
            
            allowed_extensions = ['.pdf', '.txt']
            file_extension = file.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError('Only PDF and TXT files are allowed.')
        
        return file 