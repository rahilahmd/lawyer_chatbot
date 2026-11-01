from django.db import models

# Create your models here.
class NearByPolicestation(models.Model):
    near_by_ps_id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)
    pincode = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'near_by_policestation'
