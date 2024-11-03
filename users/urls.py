from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register_page, name='register'),
    path('account/new/doctor', views.create_doc_account, name='create_doc_account'),
    path('account/new/patient', views.register_patient_account, name='register_patient'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard', views.user_dash, name='user_dashboard'),
    path('profile', views.user_profile, name='user_profile'),
    path('profile-update', views.user_profile_update, name='user_profile_update'),
    path('appointments', views.appointments, name='user_appointments'),
    path('appointment/<int:appt_id>', views.appointment, name='appointment_details'),
    path('appointment/<int:appt_id>/remarks', views.post_or_update_remarks_for_patient, name='patients_remarks')
    
]
