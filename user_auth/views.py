from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserUpdateForm
from .models import UserProfile
from main_app.models import DetectionResult, UserActivity

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_auth/signup.html'
    success_url = reverse_lazy('user_auth:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'user_auth/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log user activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='login',
            description=f'User {self.request.user.username} logged in',
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        messages.success(self.request, f'Welcome back, {self.request.user.first_name}!')
        return response
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

@login_required
def logout_view(request):
    # Log user activity before logout
    UserActivity.objects.create(
        user=request.user,
        activity_type='logout',
        description=f'User {request.user.username} logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Perform logout
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('main_app:home')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def profile_view(request):
    # Ensure UserProfile exists for the current user
    print("helloooooooooooooooooooooooooooooooooooooooooo")
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    print("user Id: ", request.user.id)
    
    # Always initialize forms with current user data
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'update_account' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Account information updated successfully!')
                return redirect('user_auth:profile')
            # If form is invalid, user_form will have errors and POST data
        elif 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile details updated successfully!')
                return redirect('user_auth:profile')
            # If form is invalid, profile_form will have errors and POST data
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    print(context['profile_form'])
    print("*"*100)
    print(context['user_form'])
    return render(request, 'user_auth/profile.html', context)

@login_required
def dashboard_view(request):
    # Get user's recent detection results
    recent_detections = request.user.detectionresult_set.all()[:10]
    
    # Get user's recent activities
    recent_activities = request.user.useractivity_set.all()[:10]
    
    # Calculate statistics
    total_scans = request.user.detectionresult_set.count()
    threats_detected = request.user.detectionresult_set.filter(result='dangerous').count()
    safe_items = request.user.detectionresult_set.filter(result='safe').count()
    total_activities = request.user.useractivity_set.count()
    
    context = {
        'recent_detections': recent_detections,
        'recent_activities': recent_activities,
        'total_scans': total_scans,
        'threats_detected': threats_detected,
        'safe_items': safe_items,
        'total_activities': total_activities,
    }
    return render(request, 'user_auth/dashboard.html', context)
