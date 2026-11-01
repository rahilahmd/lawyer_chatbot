from django.db import models

# Create your models here.
class UserRegister(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=25)
    email = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=45)
    dob = models.DateField(db_column='DOB')  # Field name made lowercase.
    user_name = models.CharField(max_length=15)
    password = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'user_register'