from django.shortcuts import render
from user_register.models import UserRegister
from login.models import Login

def userregister(request):

    if request.method == 'POST':
        obj = UserRegister()
        obj.user_name = request.POST.get('user_name')
        obj.full_name = request.POST.get('full_name')
        obj.email = request.POST.get('email')
        obj.phone_number = request.POST.get('phone_number')
        obj.age = request.POST.get('age')
        obj.gender = request.POST.get('gender')
        obj.address = request.POST.get('address')
        obj.dob = request.POST.get('dob')
        obj.password = request.POST.get('password')
        obj.save()

        ob = Login()
        ob.username = obj.user_name
        ob.password = obj.password
        ob.type = 'user'
        ob.uid = obj.user_id
        ob.save()

        return render(request, 'user_register/userregister.html', {'success': True})

    # ✅ VERY IMPORTANT — must always return something
    return render(request, 'user_register/userregister.html')
def viewuserdetails(request):
    obj=UserRegister.objects.all()
    context = {
        'uu':obj

    }
    return render(request,'user_register/viewuserdetails.html',context)