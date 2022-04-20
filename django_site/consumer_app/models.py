from django.db import models
from django_site.accounts.models import Account

# Create your models here.
class Consumer(models.Model):
    acount = models.OneToOneField(Account, primary_key=True)
    residence = models.CharField(max_length=50)
    height = models.FloatField()
    weight = models.IntegerField()
    units = models.CharField(max_length=1)
    gender = models.CharField(max_length=10)
    goal = models.CharField(max_length=50)

class Dispenser(models.Model):
    serial_num = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=50)
    consumer = models.ForeignKey(Consumer)
    registration_date = models.DateTimeField()

# class Pod(models.Model):
#     serial_num = models.CharField(max_length=100, unique=True)
#     consumer = models.ForeignKey(Consumer)
#     pod_type = models.ForeignKey(PodType)
#     remainder = models.IntegerField()

# class Regimen(models.Model):
#     consumer = models.OneToOneField(Consumer)
#     pod_type = models.ForeignKey(PodType)
#     day = models.IntegerField()
#     time = models.TimeField()
#     amount = models.FloatField

# class Dosing(models.Model):
#     pod = models.ForeignKey(Pod)
#     time = models.DateTimeField()
#     latitude = models.FloatField()
#     longitude = models.FloatField()

# class Feedback(models.Model):
#     dosing = models.OneToOneField(Dosing)
#     rating = models.IntegerField()
#     comment = models.CharField(max_length=200)

# class FeedbackReminder(models.Model):
#     dosing = models.OneToOneField(Dosing)
#     time = models.DateTimeField()

# #Company
# class Business(models.Model):
#     name = models.CharField(max_length=50)
#     docs_path = models.CharField(max_length=200)
#     # first_rep = models.ForeignKey('Representative')

# class Representative(models.Model):
#     account = models.OneToOneField(Account, primary_key=True)
#     business = models.ForeignKey(Business)
#     can_appoint_reps = models.BooleanField()


# class Company(models.Model):
#     business = models.OneToOneField(Business, primary_key=True)


# class PodType(models.Model):
#     company = models.ForeignKey(Company)
#     name = models.CharField(max_length=100)
#     substance = models.CharField(max_length=100)
#     description = models.CharField(max_length=500)
#     url = models.CharField(max_length=100)


# #Voyager Manager
# class VoyagerManager(models.Model):
#     account = models.OneToOneField(Account, primary_key=True)
#     can_appoint = models.BooleanField()
