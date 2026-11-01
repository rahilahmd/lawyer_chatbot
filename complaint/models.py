from django.db import models
from user_register.models import UserRegister
# Create your models here.
class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    # user_id = models.IntegerField()
    user=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    complaint_replay = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'complaint'
