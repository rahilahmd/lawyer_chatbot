from django.shortcuts import render
from feedback_table.models import FeedbackTable
from user_register.models import UserRegister
import datetime
# def index(request):
    # feedback_table=FeedbackTable.objects.all()
# Create your views here
def feedback_table(request):
    if request.method == "POST":
        obj=FeedbackTable()
        obj.user_id=1
        obj.date=datetime.datetime.today()
        obj.time=datetime.datetime.today()
        obj.feedback_text=request.POST['feedback_text']
        obj.rating=request.POST['rating']
        obj.save()
    return render(request, 'feedback_table/feedback.html')
def viewfeedback(request):
    obj=FeedbackTable.objects.all()
    context={
        'gg':obj
    }
    return render(request, 'feedback_table/viewfeedback.html',context)