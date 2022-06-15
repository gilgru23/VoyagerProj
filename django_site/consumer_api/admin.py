from django.contrib import admin

from .models import Consumer, Dispenser, Business, Representative

from .models import *

# Register your models here.
admin.site.register(Consumer)
admin.site.register(Dispenser)
admin.site.register(Business)
admin.site.register(Representative)
admin.site.register(Company)
admin.site.register(PodType)
admin.site.register(Pod)
admin.site.register(Regimen)
admin.site.register(Dosing)
admin.site.register(Feedback)
admin.site.register(FeedbackReminder)
admin.site.register(Caregiver)
