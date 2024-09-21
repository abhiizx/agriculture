from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from django.core.mail import send_mail
from django.http import HttpResponse



# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            login(request, user)  # Log the user in automatically after signup
            return redirect('home')  # Redirect to the home page after successful signup
        else:
            print(form.errors)  # Print form errors if validation fails
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')

    
class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    
def send_test_email(request):
    send_mail(
        'Test Subject',
        'Test message.',
        'your_email@example.com',
        ['recipient@example.com'],
        fail_silently=False,
    )
    return HttpResponse('Email sent!')