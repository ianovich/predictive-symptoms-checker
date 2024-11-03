from django.contrib import admin
from .models import Role, UserModel, Specialities, UserMeta

# Register your models here.

admin.site.register(UserModel)
admin.site.register(Role)
admin.site.register(Specialities)
admin.site.register(UserMeta)