from django.shortcuts import render
from django.db.models import Count, F, Q
from users.models import UserModel, Specialities
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .models import Appointment
from django.http import Http404

# Create your views here.
def get_doctors_with_service_price():
    # Annotate the queryset with the count of doctors and select related usermeta for role_id = 1
    doctors_with_service_price = UserModel.objects.filter(
        role_id=1
    ).annotate(
        total_doctors=Count('id'),
        service_price=F('meta__service_price'),
        doc_speciality=F('speciality__name'),
    ).select_related('meta', 'speciality')

    # Get the total number of doctors
    total_doctors = doctors_with_service_price.aggregate(total=Count('id'))

    return total_doctors['total'], list(doctors_with_service_price.values())

def get_doctors_with_speciality(speciality):
    # Annotate the queryset with the count of doctors and select related usermeta for role_id = 1
    doctors_with_service_price = UserModel.objects.filter(
        role_id=1,
        speciality__name=speciality
    ).annotate(
        total_doctors=Count('id'),
        service_price=F('meta__service_price'),
        doc_speciality=F('speciality__name'),
    ).select_related('meta', 'speciality')

    # Get the total number of doctors
    total_doctors = doctors_with_service_price.aggregate(total=Count('id'))

    return total_doctors['total'], list(doctors_with_service_price.values())

def get_doctor_with_service_price(doctor_id):
    # Get the UserModel instance by ID
    doctor = get_object_or_404(UserModel, id=doctor_id, role_id=1)
    
    # Check if the doctor has associated meta data
    if hasattr(doctor, 'meta'):
        # Annotate the doctor object with service price
        doctor.service_price = doctor.meta.service_price
    else:
        # If no meta data is found, set service price to None or handle it as needed
        doctor.service_price = None
    
    # Check if the doctor has associated speciality
    if hasattr(doctor, 'speciality'):
        # Annotate the doctor object with speciality
        doctor.doc_speciality = doctor.speciality
    else:
        # If no speciality is found, set doc_speciality to None or handle it as needed
        doctor.doc_speciality = None
    
    return doctor

#fetch all specialities
def get_specialities():
    specialities = Specialities.objects.all()
    return specialities
    


def get_available_time_slots_for_doc(date):
        # Define working hours and appointment duration
        working_hours_start = datetime.strptime('08:00', '%H:%M')  # Adjust to the doctor's working hours
        working_hours_end = datetime.strptime('17:00', '%H:%M')  # Adjust to the doctor's working hours
        appointment_duration = timedelta(minutes=30)  # Duration in minutes

        # Create a range of time slots for the given date
        time_slots = []
        current_time = working_hours_start

        while current_time < working_hours_end:
            end_time = current_time + appointment_duration

            # Check if the time slot is available (not overlapping with existing appointments)
            if Appointment.is_time_slot_available(None, date, current_time, end_time):
                time_slots.append({
                        'start': current_time.strftime('%H:%M'),
                        'end': end_time.strftime('%H:%M'),
                    })

            current_time += appointment_duration

        return time_slots
    
# def get_user_appointments(user):
#     if user.role_id == 1:
#         appointments = Appointment.objects.filter(doctor=user, status='Scheduled')
#         total_appointments = appointments.count()
#         appointments_list = appointments
        
#     elif user.role_id == 2:
#         appointments = Appointment.objects.filter(patient=user, status='Pending')
#         total_appointments = appointments.count()
#         appointments_list = appointments
#     else:
#         total_appointments = 0
#         appointments_list = []

#     return {'total_appointments': total_appointments, 'appointments_list': appointments_list}    


#fetch appointments with query optimization
def get_scheduled_appointments(user):
    if user.role_id == 1:
        # Fetch appointments for doctors
        appointments = Appointment.objects.filter(doctor=user).select_related('doctor__meta')
        # total_appointments = appointments.count()
        scheduled_appointments_count = appointments.filter(status='Scheduled').count()
        appointments_list = appointments
        # Create a dictionary to store appointments and service prices
        # appointments_list = [{'appointment': appt, 'service_price': appt.doctor.meta.service_price} for appt in appointments]
        
    elif user.role_id == 2:
        # Fetch appointments for patients
        appointments = Appointment.objects.filter(patient=user).select_related('doctor__meta')
        # total_appointments = appointments.count()
        scheduled_appointments_count = appointments.filter(status='Scheduled').count()
        appointments_list = appointments
        # Create a dictionary to store appointments and service prices
        # appointments_list = [{'appointment': appt, 'service_price': appt.doctor.meta.service_price} for appt in appointments]
    else:
        total_appointments = 0
        appointments_list = []

    return {'total_appointments': scheduled_appointments_count, 'appointments_list': appointments_list}

# def get_appointment(appt_id):
#     appointment = Appointment.objects.filter(id=appt_id).select_related('doctor__meta')
#     if appointment is not None:
#         return {'appointment': appointment}
#     else:
#         return {'There is no appointment associated with such id'}


# def get_appointment(appt_id):
#     appointment = Appointment.objects.filter(id=appt_id).select_related('doctor__meta').first()
#     if appointment is not None:
#         return appointment
#     else:
#         raise Http404("Appointment does not exist")

def get_appointment(appt_id):
    appointment = Appointment.objects.filter(id=appt_id).select_related('doctor__meta').first()
    return appointment

# def get_appointment(appt_id):
#     try:
#         appointment = Appointment.objects.filter(id=appt_id).select_related('doctor__meta').first()
#         return appointment
#     except Appointment.DoesNotExist:
#         raise Http404("Appointment does not exist")



