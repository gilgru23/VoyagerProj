from django.db import models

#Account is intentionally decoupled from the User model.
#this is to reduce django dependency and seperate all auth related data in general
class Account(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)#todo: consider making unique?
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fname + ' ' + self.lname + ' ' + self.email