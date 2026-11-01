from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.template.context_processors import request

from hearing_date.models import HearingDate
import datetime
# Create your views here
def hearingdetails(request):
    if request.method == "POST":
        obj=HearingDate()
        obj.hearing_date_time=request.POST.get('hearing_date_time')
        obj.user_id=1
        obj.lawyer_id=1
        obj.appointment_id=1
        obj.court_name=request.POST.get('court_name')
        obj.court_address=request.POST.get('court_address')
        obj.hearing_date_and_time=datetime.datetime.today()
        obj.save()
    return render(request,'hearing_date/hearing.html')

def viewhearingdetails(request):
    obj=HearingDate.objects.all()
    context={
        'hr':obj
    }
    return render(request,'hearing_date/viewhearingdetails.html',context)
def updatehearingdetails(request, idd):
    obj = HearingDate.objects.get(hearing_id=idd)
    context = {
            'ij': obj
       }
    if request.method == "POST":
        obj=HearingDate()
        obj.hearing_date_time=request.POST.get('hearing_datetime')
        obj.user_id=1
        obj.lawyer_id=1
        obj.appointment_id=1
        obj.court_name=request.POST.get('court_name')
        obj.court_address=request.POST.get('court_address')
        obj.hearing_date_and_time=datetime.datetime.today()
        obj.save()
    return render(request,'hearing_date/updatehearing.html',context)

