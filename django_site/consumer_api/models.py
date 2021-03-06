from django.utils import timezone
from django.db import models
from account_api.models import Account



# Create your models here.
class Consumer(models.Model):
    class Unit(models.IntegerChoices):
        METRIC = 1
        IMPERIAL = 2

    class Gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3

    account = models.OneToOneField(Account, primary_key=True, parent_link=True, on_delete=models.CASCADE)
    residence = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=6, decimal_places=3)
    weight = models.IntegerField()
    units = models.IntegerField(choices=Unit.choices)
    gender = models.IntegerField(choices=Gender.choices)
    obj_version = models.IntegerField(default=0)
    # goal = models.CharField(max_length=50)

    def __str__(self):
        return str(self.pk)
        # act : Account = self.account
        # return act.f_name + ' ' + act.l_name + ' ' + act.email


class Dispenser(models.Model):
    serial_num = models.CharField(max_length=100, unique=True, null=False)
    version = models.CharField(max_length=50, null=False)
    consumer = models.ForeignKey(Consumer, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    registration_date = models.DateTimeField(null=True, blank=True, default=None)
    obj_version = models.IntegerField(default=0)

    def __str__(self):
        return self.serial_num


# Company
class Business(models.Model):
    name = models.CharField(max_length=50, unique=True)
    docs_path = models.CharField(max_length=200, null=True, blank=True)

    # first_rep = models.ForeignKey('Representative')
    def __str__(self):
        return "Business: " + self.name


class Representative(models.Model):
    account = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    can_appoint_reps = models.BooleanField()

    def __str__(self):
        return str(self.pk)


class Company(models.Model):
    business = models.OneToOneField(Business, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class PodType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    substance = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Pod(models.Model):
    serial_num = models.CharField(max_length=100, unique=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)
    pod_type = models.ForeignKey(PodType, on_delete=models.CASCADE, null=False)
    remainder = models.FloatField(null=True, blank=True)
    obj_version = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pod_type) + " " + self.serial_num


class Regimen(models.Model):
    consumer = models.OneToOneField(Consumer, on_delete=models.CASCADE)
    pod_type = models.ForeignKey(PodType, on_delete=models.CASCADE)
    day = models.IntegerField()
    time = models.TimeField()
    amount = models.FloatField

    def __str__(self):
        return str(self.consumer) + " regimen"


class Dosing(models.Model):
    pod = models.ForeignKey(Pod, on_delete=models.CASCADE)
    time = models.DateTimeField()
    amount = models.FloatField(default="0.0")
    latitude = models.FloatField()
    longitude = models.FloatField()


class Feedback(models.Model):
    dosing = models.OneToOneField(Dosing, on_delete=models.CASCADE)
    rating = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=200, null=True, blank=True)


class FeedbackReminder(models.Model):
    dosing = models.OneToOneField(Dosing, on_delete=models.CASCADE)
    time = models.DateTimeField()


class Caregiver(models.Model):
    account = models.OneToOneField(Account, primary_key=True, parent_link=True, on_delete=models.CASCADE)
    consumers = models.ManyToManyField(Consumer, blank=True, default=None)

    def __str__(self):
        return str(self.pk)

# Voyager Manager
# class VoyagerManager(models.Model):
#     account = models.OneToOneField(Account, primary_key=True)
#     can_appoint = models.BooleanField()
