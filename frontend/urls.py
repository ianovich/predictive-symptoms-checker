from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('services', views.services, name='services'),
    path('contacts', views.contacts, name='contacts'),
    path('doctors', views.doctors, name='doctors'),
    path('symptom-checker', views.symptom_checker, name='symptom_checker'),
    path('doctor/<int:doctor_id>', views.doctor, name='doctor_details'),
    path('book-appointment/doctor/<int:doctor_id>/<str:date>/', views.book_appointment, name='book-appointment'),
    path('doctors/speciality/<str:speciality>', views.doctors_with_specialiy, name='doctors-with-speciality'),
]
