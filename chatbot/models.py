from django.db import models
from user_register.models import UserRegister

# Create your models here.
class Chatbot(models.Model):
    chatbot_id = models.AutoField(primary_key=True)
    message = models.TextField()
    # user = models.CharField(max_length=45)
    user=models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    date = models.DateTimeField()
    replay = models.TextField()

    class Meta:
        managed = False
        db_table = 'chatbot'

    def __str__(self):
        return self.message[:50]