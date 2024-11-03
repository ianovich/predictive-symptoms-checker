from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import UserModel, UserMeta
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from decimal import Decimal, InvalidOperation
from doctors.views import get_scheduled_appointments, get_specialities, get_appointment
from django.http import Http404

# def login_page(request):
  
#     context = {
#         "title": "Login User"
#     }
#     return render(request,'frontend/auth/login.html', context=context)

def register_page(request):
    
  
    context = {
        "title": "Register User",
    }
    return render(request,'frontend/auth/register.html', context=context)

#logout user
def logout_user(request):
    logout(request)
    return redirect('home')

#create doctor
def create_doc_account(request):
    specialities = get_specialities
    if request.method == 'POST':
        required_fields = ['email', 'first_name', 'last_name', 'phone', 'speciality_id', 'location', 'password', 'conf_password']
        
        # Check if all required fields are present in the POST data
        if all(request.POST.get(field) for field in required_fields):
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            speciality_id = request.POST['speciality_id']
            location = request.POST['location']
            password = request.POST['password']
            conf_password = request.POST['conf_password']
            role_id = 1  # Assuming role_id is a constant value or retrieved from somewhere
            # service_price = request.POST['service_price']
            
            # Extract username from email
            username = email.split('@')[0]
            
            # Check if passwords match
            if password != conf_password:
                messages.error(request, 'Passwords do not match')
            elif len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
            else:
                # Flag to track if any error occurred
                error_occurred = False
                # Check if email and phone are unique
                if UserModel.objects.filter(email=email).exists():
                    messages.error(request, 'A user with that email address already exists.')
                    error_occurred = True
                if UserModel.objects.filter(phone=phone).exists():
                    messages.error(request, 'A user with that phone number already exists.')
                    error_occurred = True
                if not error_occurred:
                    # Create user with extracted username
                    doc = UserModel.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone, speciality_id=speciality_id, location=location, role_id=role_id)
                    # Additional fields can be set here if needed
                    doc.save()
                    
                    service_price = request.POST.get('service_price')
                    # Ensure service price is provided and is a valid number
                    if service_price:
                        try:
                            service_price_decimal = Decimal(service_price)
                        except InvalidOperation:
                            service_price_decimal = None
                        # Create or update UserMeta instance
                        # user_meta, created = UserMeta.objects.get_or_create(user=doc.id)
                        user_meta, created = UserMeta.objects.get_or_create(user_id=doc.id)
                        user_meta.service_price = service_price_decimal
                        user_meta.save()
                    # messages.success(request, 'User created successfully')
                    return redirect('login')
        else:
            messages.error(request, 'Please fill out all required fields')
    
        return redirect('create_doc_account')
    else:
        context = {
            "title": "Register Doctor",
            "specialities": specialities,
        }
        return render(request, 'frontend/auth/reg_doc.html', context=context)
    

#create patient account
def register_patient_account(request):
    if request.method == 'POST':
        required_fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'conf_password']
        
        # Check if all required fields are present in the POST data
        if all(request.POST.get(field) for field in required_fields):
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            password = request.POST['password']
            conf_password = request.POST['conf_password']
            role_id = 2  # Assuming role_id is a constant value or retrieved from somewhere
            
            # Extract username from email
            username = email.split('@')[0]
            
            # Check if passwords match
            if password != conf_password:
                messages.error(request, 'Passwords do not match')
            elif len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
            else:
                # Flag to track if any error occurred
                error_occurred = False
                # Check if email and phone are unique
                if UserModel.objects.filter(email=email).exists():
                    messages.error(request, 'A user with that email address already exists.')
                    error_occurred = True
                if UserModel.objects.filter(phone=phone).exists():
                    messages.error(request, 'A user with that phone number already exists.')
                    error_occurred = True
                if not error_occurred:
                    # Create user with extracted username
                    patient = UserModel.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone, role_id=role_id)
                    # Additional fields can be set here if needed
                    patient.save()
                    # messages.success(request, 'User created successfully')
                    return redirect('login')
        else:
            messages.error(request, 'Please fill out all required fields')
    
        return redirect('register_patient')
    else:
        context = {
            "title": "Register Patient"
        }
        return render(request, 'frontend/auth/reg_patient.html', context=context)
    

#login user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print("Email:", email)  # Debug output
        print("Password:", password)  # Debug output

      # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
                # User authentication successful
            login(request, user)
                # Redirect to the home page or any desired page
            return redirect('home')
        else:
          # Check if a user with the provided email exists
          user_by_email = UserModel.objects.filter(email=email).exists()
          if user_by_email:
                # Maintain the entered email value in the form
                context = {
                    'title': 'Login User',
                    'email': email,
                }
                messages.error(request, 'The password you provided is incorrect')
                return render(request, 'frontend/auth/login.html', context=context)
          else:
                # Email does not exist in the database
                messages.error(request, 'No user found with this email')
                return redirect('login')
    else:
        # Handle GET request (if needed)
        context = {
            "title": "Login User"
        }
        return render(request, 'frontend/auth/login.html', context=context)
    
#user dashboard
@login_required(login_url='login')
def user_dash(request):
    user = request.user
    total_appointments = get_scheduled_appointments(user)
  
    context = {
        "title": "User Dashboard",
        "total_appointments": total_appointments,
    }
    return render(request,'frontend/user/dashboard.html', context=context)

@login_required(login_url='login')
def user_profile(request):
  
#   if request.method == 'GET':
    context = {
        "title": "User Profile"
    }
    return render(request,'frontend/user/profile.html', context=context)

@login_required(login_url='login')
def user_profile_update(request):
    if request.method == 'POST':
        # Fetch the existing user profile data
        user = request.user
        # Update the fields with the new data submitted in the form
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.location = request.POST.get('location', user.location)
        # user.user_bio = request.POST.get('user_bio', user.user_bio)
        # Trim white spaces from the user bio
        user_bio = request.POST.get('user_bio', '').strip()
        user.user_bio = user_bio if user_bio else None  # Set to None if bio is empty after stripping
        # Check if profile image is uploaded and update if necessary
        # if 'profile_image' in request.FILES:
        #     user.profile_url = request.FILES['profile_image']
        # # Save the updated user profile data
        # user.save()
        
        if 'profile_image' in request.FILES:
            new_profile_image = request.FILES['profile_image']
            # Check if an existing profile image exists
            if user.profile_url:
                # If an existing profile image exists, delete it
                os.remove(os.path.join(settings.MEDIA_ROOT, str(user.profile_url)))
            user.profile_url = new_profile_image
        # Save the updated user profile data
        user.save()
        
        # If the current user's role_id is 1, add the service price to UserMeta
        if user.role_id == 1:
            service_price = request.POST.get('service_price')
            # Ensure service price is provided and is a valid number
            if service_price:
                try:
                    service_price_decimal = Decimal(service_price)
                except InvalidOperation:
                    service_price_decimal = None
                # Create or update UserMeta instance
                user_meta, created = UserMeta.objects.get_or_create(user=user)
                user_meta.service_price = service_price_decimal
                user_meta.save()
        
        # Redirect to a success page or user profile page
        return redirect('user_profile')
    
    
@login_required(login_url='login')
def appointments(request):
    user = request.user
    appointments_list = get_scheduled_appointments(user)
    
    context = {
        "title": "Appointments",
        "appointments_list": appointments_list
    }
    
    return render(request, 'frontend/user/user_appointments.html', context=context)

# @login_required(login_url='login')
# def appointment(request, appt_id):
#     appointment = get_appointment(appt_id)
#     context = {
#         "title": "Appointment",
#         "appointment": appointment
#     }
#     return render(request, 'frontend/user/appointment.html', context=context)

@login_required(login_url='login')
def appointment(request, appt_id):
    appointment = get_appointment(appt_id)
    if appointment is None:
        error_message = "Appointment does not exist"
    else:
        error_message = None

    context = {
        "title": "Appointment",
        "appointment": appointment,
        "error_message": error_message,
    }
    return render(request, 'frontend/user/user_appointment.html', context=context)

#add or update func for patient remarks.
@login_required(login_url='login')
def post_or_update_remarks_for_patient(request, appt_id):
    # Get the appointment object
    appointment = get_appointment(appt_id)

    # Check if the appointment exists
    if appointment is None:
        error_message = "Appointment does not exist"
        # Handle the case where the appointment does not exist, for example:
        # return HttpResponseNotFound("Appointment does not exist")
    else:
        error_message = None
    
        # Update appointment remarks from the form data, or keep existing remarks if form data is empty
        appointment.remarks = request.POST.get('remarks')
        # Change status to "Visited"
        appointment.status = "Visited"
        appointment.save()
        
        # Add a success message
        messages.success(request, 'Remarks updated successfully.')
    
    # Redirect to the appropriate view (replace 'appointment_details' with the correct URL name)
    return redirect('appointment_details', appt_id=appt_id)
        
    

    