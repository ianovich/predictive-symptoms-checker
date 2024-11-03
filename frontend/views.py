from django.shortcuts import render, redirect
from doctors.views import get_doctors_with_service_price, get_doctor_with_service_price, get_available_time_slots_for_doc, get_doctors_with_speciality
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
import pytz
from datetime import datetime
from doctors.models import Appointment
from users.models import UserModel
from django.urls import reverse
import joblib

# Create your views here.

#load the training model
model = joblib.load('trained_symptom_disease_predictor_model')

symptoms = [
    "itching",
    "skin_rash",
    "nodal_skin_eruptions",
    "continuous_sneezing",
    "shivering",
    "chills",
    "joint_pain",
    "stomach_pain",
    "acidity",
    "ulcers_on_tongue",
    "muscle_wasting",
    "vomiting",
    "burning_micturition",
    "spotting_ urination",
    "fatigue",
    "weight_gain",
    "anxiety",
    "cold_hands_and_feets",
    "mood_swings",
    "weight_loss",
    "restlessness",
    "lethargy",
    "patches_in_throat",
    "irregular_sugar_level",
    "cough",
    "high_fever",
    "sunken_eyes",
    "breathlessness",
    "sweating",
    "dehydration",
    "indigestion",
    "headache",
    "yellowish_skin",
    "dark_urine",
    "nausea",
    "loss_of_appetite",
    "pain_behind_the_eyes",
    "back_pain",
    "constipation",
    "abdominal_pain",
    "diarrhoea",
    "mild_fever",
    "yellow_urine",
    "yellowing_of_eyes",
    "acute_liver_failure",
    "fluid_overload",
    "swelling_of_stomach",
    "swelled_lymph_nodes",
    "malaise",
    "blurred_and_distorted_vision",
    "phlegm",
    "throat_irritation",
    "redness_of_eyes",
    "sinus_pressure",
    "runny_nose",
    "congestion",
    "chest_pain",
    "weakness_in_limbs",
    "fast_heart_rate",
    "pain_during_bowel_movements",
    "pain_in_anal_region",
    "bloody_stool",
    "irritation_in_anus",
    "neck_pain",
    "dizziness",
    "cramps",
    "bruising",
    "obesity",
    "swollen_legs",
    "swollen_blood_vessels",
    "puffy_face_and_eyes",
    "enlarged_thyroid",
    "brittle_nails",
    "swollen_extremeties",
    "excessive_hunger",
    "extra_marital_contacts",
    "drying_and_tingling_lips",
    "slurred_speech",
    "knee_pain",
    "hip_joint_pain",
    "muscle_weakness",
    "stiff_neck",
    "swelling_joints",
    "movement_stiffness",
    "spinning_movements",
    "loss_of_balance",
    "unsteadiness",
    "weakness_of_one_body_side",
    "loss_of_smell",
    "bladder_discomfort",
    "foul_smell_of urine",
    "continuous_feel_of_urine",
    "passage_of_gases",
    "internal_itching",
    "toxic_look_(typhos)",
    "depression",
    "irritability",
    "muscle_pain",
    "altered_sensorium",
    "red_spots_over_body",
    "belly_pain",
    "abnormal_menstruation",
    "dischromic _patches",
    "watering_from_eyes",
    "increased_appetite",
    "polyuria",
    "family_history",
    "mucoid_sputum",
    "rusty_sputum",
    "lack_of_concentration",
    "visual_disturbances",
    "receiving_blood_transfusion",
    "receiving_unsterile_injections",
    "coma",
    "stomach_bleeding",
    "distention_of_abdomen",
    "history_of_alcohol_consumption",
    "fluid_overload",
    "blood_in_sputum",
    "prominent_veins_on_calf",
    "palpitations",
    "painful_walking",
    "pus_filled_pimples",
    "blackheads",
    "scurring",
    "skin_peeling",
    "silver_like_dusting",
    "small_dents_in_nails",
    "inflammatory_nails",
    "blister",
    "red_sore_around_nose",
    "yellow_crust_ooze"
]

def index(request):
    """This function is used to render the index page"""

    context = {
        "title": "Home",
    }

    return render(request, "frontend/index.html", context=context)

def services(request):
    context = {
        "title": "Services",
         "bc_title": "Services",
    }

    return render(request, "frontend/services.html", context=context)

def contacts(request):
    context = {
        "title": "Contact Us",
        "bc_title": "Contact Us",
    }

    return render(request, "frontend/contacts.html", context=context)

def doctors(request):
    total_doctors, doctors_info = get_doctors_with_service_price()
    
    context = {
        "title": "Doctors",
        "bc_title": "Doctors",
        "total_doctors": total_doctors,
        "doctors_info": doctors_info,
    }

    return render(request, "frontend/doctors.html", context=context)


def doctors_with_specialiy(request, speciality):
    total_doctors, doctors_info = get_doctors_with_speciality(speciality)
    
    context = {
        "title": "Doctors",
        "bc_title": "Doctors",
        "total_doctors": total_doctors,
        "doctors_info": doctors_info,
    }

    return render(request, "frontend/doctors.html", context=context)

def doctor(request, doctor_id):
    doctor = get_doctor_with_service_price(doctor_id)
    
    if not doctor:
        # Handle doctor not found
        return render(request, "frontend/404.html")  
    
    # Set the time zone to Nairobi (EAT)
    time_zone = 'Africa/Nairobi'
    timezone.activate(pytz.timezone(time_zone))
    
    todays_date = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    selected_date = request.GET.get('date', todays_date)
    
    # Get the selected week's date range in Nairobi time zone
    start_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
    # Calculate start of the week
    start_of_week = start_date - timezone.timedelta(days=start_date.weekday())  
    end_date = start_of_week + timezone.timedelta(days=6)

    
    # Generate date range for a week
    date_range = [start_of_week + timezone.timedelta(days=i) for i in range(7)]
    
     # Get the selected date in Nairobi time zone
    selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
    
     # Fetch available time slots for the selected date
    available_time_slots = {
        selected_date.strftime('%Y-%m-%d'): get_available_time_slots_for_doc(selected_date.strftime('%Y-%m-%d'))
    }
    
    # Fetch booked slots for the selected date
    booked_slots = Appointment.get_booked_slots(doctor, selected_date)

    context = {
        "title": f"Dr. {doctor.first_name} {doctor.last_name}",
        "bc_title": f"Dr. {doctor.first_name} {doctor.last_name}",
        "doctor": doctor,
        'available_time_slots': available_time_slots,
        'booked_slots': booked_slots,
        'start_date': start_date,
        'end_date': end_date,
        'todays_date': todays_date,
        'selected_date': selected_date,
        'date_range': date_range,
    }

    return render(request, "frontend/doctor.html", context=context)

def book_appointment(request, doctor_id, date):
    if request.method == 'POST':
        # Validate the form data
        selected_slot = request.POST.get('selected_slot')

        if date and selected_slot is not None:
            doctor = UserModel.objects.get(id=doctor_id)
            patient = request.user  # Assuming the patient is authenticated

            appointment_time = selected_slot
            appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    date=date,
                    appointment_time=appointment_time,
                    status='Scheduled'
                )
            messages.success(request, 'Appointment booked successfully!')

                # Redirect to a confirmation page or do something else
            # return redirect('/')
            return redirect(reverse('doctor_details', kwargs={'doctor_id': doctor_id}))
        else:
            # Handle missing form data or invalid slot index
            # return redirect('/')  # Redirect to an appropriate view
            messages.error(request,' Missing form data or invalid slot index')
            return redirect(reverse('doctor_details', kwargs={'doctor_id': doctor_id}))
    else:
        # Handle non-POST requests
        return redirect('/')  # Redirect to an appropriate view


def symptom_checker(request):
     
    # Add indices to each symptom
    symptoms_with_indices = [(index, symptom) for index, symptom in enumerate(symptoms)]
    
    if request.method == 'POST':
        selected_indices_symp = request.POST.getlist('selected_indices[]')
        selected_symptoms = [symptoms[int(index)] for index in selected_indices_symp]
            
        a = list(range(0,132))
        
        # Input symptoms from the user
        selected_indices = [int(index) for index in request.POST.getlist('selected_indices[]')]
        
        b = [int(x) for x in selected_indices]
        count = 0
        while count < len(b):
            item_to_replace =  b[count]
            replacement_value = 1
            indices_to_replace = [i for i,x in enumerate(a) if x==item_to_replace]
            count += 1
            for i in indices_to_replace:
                a[i] = replacement_value
        a = [0 if x !=1 else x for x in a]
        y_diagnosis = model.predict([a])
        y_pred_2 = model.predict_proba([a])
        # print(('Name of the infection = %s , confidence score of : = %s') %(y_diagnosis[0],y_pred_2.max()* 100),'%' )
        predicted_disease = y_diagnosis[0]
        confidencescore = y_pred_2.max()* 100
        confidence_score = format(confidencescore, '.0f')
        
        #consult_doctor codes
        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
        
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist_Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"
        
        # Pass the prediction result to the template for rendering
        context = {
            "title": "Symptoms Check",
            "bc_title": "Symptoms Check",
            "symptoms": symptoms_with_indices,
            "selected_indices": selected_indices,
            "selected_symptoms": selected_symptoms,
            "predicted_disease": predicted_disease,
            "confidence_score": confidence_score,
            "consultdoctor": consultdoctor,
        }
        return render(request, "frontend/symptom_checker.html", context=context)
        
    # Include the symptoms list in the context dictionary
    context = {
            "title": "Symptoms Check",
            "bc_title": "Symptoms Check",
            "symptoms": symptoms_with_indices,
        }

    return render(request, "frontend/symptom_checker.html", context=context)
