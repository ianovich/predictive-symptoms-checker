from django.db import models
from users.models import UserModel

class Appointment(models.Model):
    PENDING = 'pending'
    SCHEDULED = 'scheduled'
    VISITED = 'visited'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SCHEDULED, 'Scheduled'),
        (VISITED, 'Visited'),
    ]
    
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    date = models.DateField()
    appointment_time = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'appointments'
        
    @classmethod
    def is_time_slot_available(cls, doctor, date, current_time, end_time):
        # Check if any appointments exist for the given doctor, date, and time range
        existing_appointments = cls.objects.filter(
            doctor=doctor,
            date=date,
            appointment_time__gte=current_time,
            appointment_time__lt=end_time
        ).exists()

        # Return True if no appointments exist in the given time slot, else False
        return not existing_appointments

    
    @classmethod
    def get_booked_slots(cls, doctor, date):
        # Retrieve booked slots for a specific doctor and date
        booked_slots = cls.objects.filter(doctor=doctor, date=date).values_list('appointment_time', flat=True)
        return booked_slots
       
