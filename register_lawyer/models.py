# from django.db import models
#
# # Create your models here.
# class RegisterLawyer(models.Model):
#     lawyer_id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=45)
#     lawyer_qualification = models.CharField(max_length=45)
#     photo = models.CharField(max_length=1000)
#     email = models.CharField(max_length=45)
#     address = models.CharField(max_length=45)
#     user_name = models.CharField(max_length=45)
#     password = models.CharField(max_length=45)
#     age = models.IntegerField()
#     phone_number = models.CharField(max_length=45)
#     gender = models.CharField(max_length=45)
#     dob = models.DateField(blank=True, null=True)
#     lawyer_category = models.CharField(max_length=45)
#     status = models.CharField(max_length=45, blank=True, null=True)
#     certificate = models.CharField(max_length=255, blank=True, null=True)
#     bar_enrollment = models.CharField(max_length=20, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'register_lawyer'
from django.db import models


class RegisterLawyer(models.Model):
    lawyer_id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=45)
    lawyer_qualification = models.CharField(max_length=45)

    photo = models.CharField(max_length=1000)
    certificate = models.CharField(max_length=255, blank=True, null=True)

    email = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=128)

    age = models.IntegerField()
    phone_number = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)

    dob = models.DateField(blank=True, null=True)
    lawyer_category = models.CharField(max_length=45)

    status = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        default="Pending"
    )

    bar_enrollment = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'register_lawyer'

    def __str__(self):
        return self.full_name