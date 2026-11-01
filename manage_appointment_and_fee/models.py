from django.db import models
from user_register.models import UserRegister
from register_lawyer.models import RegisterLawyer
# Create your models here.
class ManageAppointmentAndFees(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    # lawyer_id = models.IntegerField()
    # user_id = models.IntegerField()
    lawyer=models.ForeignKey(RegisterLawyer,on_delete=models.CASCADE)
    user= models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50)
    case_summary = models.CharField(max_length=150)
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manage_appointment_and_fees'