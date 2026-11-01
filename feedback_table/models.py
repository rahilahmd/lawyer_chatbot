from django.db import models
from user_register.models import  UserRegister
# Create your models here.
class FeedbackTable(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    # user_id = models.IntegerField()
    user=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField(default=0)  # ⭐ NEW FIELD
    date = models.DateField()
    time = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'feedback_table'
