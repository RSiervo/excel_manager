from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
from .models import Profile  # Import your Profile model

def about(request):
    return render(request, 'accounts/about.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def services(request):
    return render(request, 'accounts/services.html')

@login_required
def restore(request):
    return render(request, 'accounts/restore.html')

@login_required
def backup(request):
    return render(request, 'accounts/backup.html')

@login_required
def save_files(request):
    return render(request, 'accounts/save_files.html')

@login_required
def upload_excel(request):
    data = None  # Default to no data initially

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Read the Excel file into a DataFrame
            try:
                df = pd.read_excel(uploaded_file)
                # Convert DataFrame to list of dictionaries for the template
                data = df.to_dict(orient="records")
                request.session['excel_data'] = json.dumps(data)  # Store data in session
                messages.success(request, "File uploaded successfully.")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
        else:
            messages.error(request, "No file uploaded.")
    
    # Load data from session if available
    if not data and 'excel_data' in request.session:
        data = json.loads(request.session['excel_data'])

    return render(request, 'accounts/upload_excel.html', {"data": data})

@login_required
def load_excel_data(request):
    # Load data from session if available
    if 'excel_data' in request.session:
        data = json.loads(request.session['excel_data'])
        return render(request, 'accounts/upload_excel.html', {"data": data})
    else:
        messages.error(request, "No data available. Please upload a file first.")
        return redirect('upload_excel')

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def save_data(request):
    # Handles the saving of edited data from the frontend
    updated_data = request.POST.get("updated_data")
    if updated_data:
        try:
            data = json.loads(updated_data)
            # Logic to save data, for example, back to Excel or a database
            # (e.g., save to a session, database, or file)
            request.session['excel_data'] = json.dumps(data)  # Update session with new data
            return JsonResponse({"message": "Data saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": f"Failed to save data: {e}"}, status=400)
    return JsonResponse({"error": "No data provided"}, status=400)

@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, "Successfully registered! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the form details.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'accounts/login.html')

#register users profile 

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Save profile picture to Profile model
            profile = Profile.objects.get(user=user)
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            profile.save()

            messages.success(request, "Successfully registered! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the form details.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
