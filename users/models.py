from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

def user_profile_image_path(instance, filename):
    # This function generates the file path for the user's profile image
    return f'user-profiles/{instance.username}/{filename}'

# roles model
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
#Specialities
class Specialities(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'specialities'

    def __str__(self):
        return self.name
    
# user model
class UserModel(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'A user with that email address already exists.'
        }
    )
    phone = models.IntegerField(
        unique=True,
        error_messages={
            'unique': 'A user with that phone number already exists.'
        }
    )

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.ForeignKey(Specialities, on_delete=models.SET_NULL, null=True, blank=True)
    profile_url = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    user_bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
    
    
# UserMeta model
class UserMeta(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='meta')
    service_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
       db_table = 'user_meta'

    def __str__(self):
        return self.user.email
