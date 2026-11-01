from django.shortcuts import render
from near_by_policestation.models import NearByPolicestation

# Create your views here.
def nearbypolicestation(request):
    if request.method == "POST":
        obj=NearByPolicestation()
        obj.near_by_ps_id=1
        obj.place=request.POST.get('place')
        obj.pincode=request.POST.get('pincode')
        obj.phone_number=request.POST.get('phone')
        obj.save()

    return render(request, 'near_by_policestation/nearbypolicestation.html')
def viewpolicestation(request):
    obj=NearByPolicestation.objects.all()
    context = {
        'yy':obj
    }
    return render(request, 'near_by_policestation/viewpolicestation.html',context)