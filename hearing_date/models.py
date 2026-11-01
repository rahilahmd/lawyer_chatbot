from django.db import models
from user_register.models import UserRegister
from register_lawyer.models import RegisterLawyer
# Create your models here.
class HearingDate(models.Model):
    hearing_id = models.AutoField(primary_key=True)
    # user_id = models.IntegerField()
    # lawyer_id = models.IntegerField()
    user=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    lawyer=models.ForeignKey(RegisterLawyer,on_delete=models.CASCADE)
    hearing_date_time = models.DateField()
    appointment_id = models.IntegerField()
    court_name = models.CharField(max_length=15)
    court_address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'hearing_date'