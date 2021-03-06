from django.db import models


# Account is intentionally decoupled from the User model.
# this is to reduce django dependency and separate all auth related data in general
class Account(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False)
    f_name = models.CharField(max_length=50, null=False)
    l_name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=20, null=False)
    dob = models.DateField(null=False)
    registration_date = models.DateField(auto_now_add=True)
    obj_version = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + ' - ' + self.email
