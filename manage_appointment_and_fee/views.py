# from django.shortcuts import render,redirect
# from manage_appointment_and_fee.models import ManageAppointmentAndFees
# import datetime
# # Create your views here.
# def appointmentandfees(request,idd):
#     ss=request.session.get('uid')
#     if request.method =='POST':
#         obj=ManageAppointmentAndFees()
#         obj.lawyer_id=idd
#         obj.user_id=ss
#         obj.full_name=request.POST.get('full_name')
#         obj.email=request.POST.get('email')
#         obj.phone_number=request.POST.get('phone_number')
#         obj.service_type=request.POST.get('service_type')
#         obj.appointment_date = request.POST.get('appointment_date')
#         obj.appointment_time = request.POST.get('appointment_time')
#         obj.case_summary=request.POST.get('case_summary')
#         obj.save()
#
#     return render(request, 'manage_appointment_and_fee/appointmentandfees.html')
# def viewappointment(request):
#     obj=ManageAppointmentAndFees.objects.filter(lawyer_id=request.session['uid'])
#     context={
#         'wp':obj
#     }
#     return render(request, 'manage_appointment_and_fee/viewappointment.html',context)
# def accept(request,idd):
#     obj=ManageAppointmentAndFees.objects.get(appointment_id=idd)
#     obj.status='accepted'
#     obj.save()
#     return viewappointment(request)
# def reject(request,idd):
#     obj=ManageAppointmentAndFees.objects.get(appointment_id=idd)
#     obj.status='rejected'
#     obj.save()
#     return viewappointment(request)
# def adminviewapp(request):
#     obj=ManageAppointmentAndFees.objects.all()
#     context={
#         'av':obj
#     }
#     return render(request, 'manage_appointment_and_fee/adminviewapp.html',context)
# def appviewuser(request):
#     obj=ManageAppointmentAndFees.objects.filter(user_id=request.session['uid'])
#     context={
#         'sv':obj
#     }
#     return render(request, 'manage_appointment_and_fee/appviewuser.html',context)
# def deleteappointment(request,idd):
#     obj=ManageAppointmentAndFees.objects.get(appointment_id=idd)
#     obj.delete()
#     return appviewuser(request)
from django.shortcuts import render, redirect
from manage_appointment_and_fee.models import ManageAppointmentAndFees
from register_lawyer.models import RegisterLawyer
from user_register.models import UserRegister


# ✅ BOOK APPOINTMENT
def appointmentandfees(request, idd):

    user_id = request.session.get('uid')

    lawyer_obj = RegisterLawyer.objects.get(pk=idd)
    user_obj = UserRegister.objects.get(pk=user_id)

    if request.method == 'POST':

        obj = ManageAppointmentAndFees()

        obj.lawyer = lawyer_obj
        obj.user = user_obj
        obj.full_name = user_obj.full_name
        obj.email = user_obj.email
        obj.phone_number = request.POST.get('phone_number')
        obj.service_type = request.POST.get('service_type')
        obj.appointment_date = request.POST.get('appointment_date')
        obj.appointment_time = request.POST.get('appointment_time')
        obj.case_summary = request.POST.get('case_summary')
        obj.status = "pending"

        obj.save()

        return render(request,
                      'manage_appointment_and_fee/appointmentandfees.html',
                      {'success': True})

    return render(request, 'manage_appointment_and_fee/appointmentandfees.html')


# ✅ LAWYER VIEW APPOINTMENTS
def viewappointment(request):

    lawyer_id = request.session.get('uid')
    lawyer_obj = RegisterLawyer.objects.get(pk=lawyer_id)

    obj = ManageAppointmentAndFees.objects.filter(lawyer=lawyer_obj)

    context = {
        'wp': obj
    }

    return render(request, 'manage_appointment_and_fee/viewappointment.html', context)


# ACCEPT APPOINTMENT
def accept(request, idd):
    obj = ManageAppointmentAndFees.objects.get(appointment_id=idd)
    obj.status = 'accepted'
    obj.save()
    return redirect('view_ap')


# REJECT APPOINTMENT
def reject(request, idd):
    obj = ManageAppointmentAndFees.objects.get(appointment_id=idd)
    obj.status = 'rejected'
    obj.save()
    return redirect('view_ap')


# ✅ ADMIN VIEW ALL
def adminviewapp(request):
    obj = ManageAppointmentAndFees.objects.all()
    context = {
        'av': obj
    }
    return render(request, 'manage_appointment_and_fee/adminviewapp.html', context)


# ✅ USER VIEW THEIR APPOINTMENTS
def appviewuser(request):

    user_id = request.session.get('uid')
    user_obj = UserRegister.objects.get(pk=user_id)

    obj = ManageAppointmentAndFees.objects.filter(user=user_obj)

    context = {
        'sv': obj
    }

    return render(request, 'manage_appointment_and_fee/appviewuser.html', context)


# ✅ DELETE APPOINTMENT
def deleteappointment(request, idd):
    obj = ManageAppointmentAndFees.objects.get(appointment_id=idd)
    obj.delete()
    return redirect('appviewuser')