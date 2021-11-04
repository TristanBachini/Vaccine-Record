from django.contrib import admin
from .models import *

admin.site.register(PatientRecord)
admin.site.register(Location)
admin.site.register(Time)
admin.site.register(Visit)
admin.site.register(Appointment)
admin.site.register(Vaccine)
