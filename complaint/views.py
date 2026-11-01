from django.shortcuts import render
from complaint.models import Complaint
# Create your views here.
def complaints(request):
    if request.method == "POST":
        obj=Complaint()
        obj.complaint=request.POST['complaint']
        obj.complaint_replay='pending'
        obj.user_id=1
        obj.save()
    return render(request, 'complaint/complaints.html')

def postcomplaintreplay(request,idd):
    if request.method == "POST":
        obj=Complaint.objects.get(complaint_id=idd)
        obj.complaint_replay=request.POST.get('reply')
        obj.save()
    return render(request, 'complaint/postcomplaintreplay.html')

def replaycomplaints(request):
    obj=Complaint.objects.all()
    context={
        'co':obj
    }
    return render(request, 'complaint/replycomplaint.html',context)
def viewcomplaints(request):
    obj=Complaint.objects.all()
    context={
        'c':obj
    }
    return render(request, 'complaint/viewcomplaints.html',context)
def replyview(request):
    obj=Complaint.objects.filter(complaint_id=request.session['uid'])
    context={
        'xx':obj
    }
    return render(request, 'complaint/replyview.html',context)