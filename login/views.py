# from login.models import Login
# from django.shortcuts import render
# from django.http import HttpResponseRedirect
#
# # Create your views here.
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         obj=Login.objects.filter(username=username,password=password)
#         print(len(obj))
#         tp = ""
#         for ob in obj:
#             tp=ob.type
#             uid=ob.uid
#             if tp == "admin":
#                 request.session["uid"]=uid
#                 return HttpResponseRedirect("/temp/admin/")
#             elif tp == "user":
#                 request.session["uid"]=uid
#                 return HttpResponseRedirect("/temp/users/")
#             elif tp == "lawyer":
#                 request.session["uid"]=uid
#                 return HttpResponseRedirect("/temp/lawyers/")
#         else:
#                 objlist = "username or password incorrect..... please try again...."
#                 context = {
#                     "m": objlist,
#                 }
#                 return render(request, 'login/login.html',context)
#     return render(request, 'login/login.html')
# def register(request):
#     obj=login(request)
#     return render(request, 'login/register.html')
# from login.models import Login
# from register_lawyer.models import RegisterLawyer
#
# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.contrib.auth.hashers import check_password
#
#
# def _fail(request, message, kind):
#     """Show the login page with a message.
#     kind: "noacct" | "wrong" | "rejected" | "pending"  (controls the animation)
#     """
#     return render(request, "login/login.html", {"m": message, "kind": kind})
#
#
# def login(request):
#
#     if request.method == "POST":
#
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         obj = Login.objects.filter(username=username)
#
#         # 1. Username does not exist -> not registered
#         if not obj.exists():
#             return _fail(request, "This account is not registered.", "noacct")
#
#         for ob in obj:
#
#             # 2. Check password
#             if check_password(password, ob.password) or password == ob.password:
#
#                 tp = ob.type
#                 uid = ob.uid
#
#                 if tp == "admin":
#
#                     request.session["uid"] = uid
#                     return HttpResponseRedirect("/temp/admin/")
#
#                 elif tp == "user":
#
#                     request.session["uid"] = uid
#                     return HttpResponseRedirect("/temp/users/")
#
#                 elif tp == "lawyer":
#
#                     # Check lawyer approval status
#                     lawyer = RegisterLawyer.objects.filter(
#                         lawyer_id=uid
#                     ).first()
#
#                     if lawyer is None:
#                         return _fail(request, "No lawyer profile was found for this account.", "noacct")
#
#                     status = (lawyer.status or "").lower()
#
#                     if status == "accepted":
#
#                         request.session["uid"] = uid
#                         return HttpResponseRedirect("/temp/lawyers/")
#
#                     elif status == "rejected":
#                         return _fail(request, "Your lawyer application has been rejected by the admin.", "rejected")
#
#                     else:
#                         return _fail(request, "Your lawyer application is still pending admin approval.", "pending")
#
#         # 3. Username exists but the password did not match
#         return _fail(request, "Incorrect password. Please try again.", "wrong")
#
#     return render(request, "login/login.html")
#
#
# def register(request):
#     return render(request, "login/register.html")
# new
from login.models import Login
from register_lawyer.models import RegisterLawyer

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password


def _fail(request, message, kind):
    """Show the login page with a message.
    kind: "noacct" | "wrong" | "rejected" | "pending"  (controls the animation)
    """
    return render(request, "login/login.html", {"m": message, "kind": kind})


def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        obj = Login.objects.filter(username=username)

        # 1. Username does not exist -> not registered
        if not obj.exists():
            return _fail(request, "This account is not registered.", "noacct")

        for ob in obj:

            # 2. Check password
            if check_password(password, ob.password) or password == ob.password:

                tp = ob.type
                uid = ob.uid

                if tp == "admin":

                    request.session["uid"] = uid
                    request.session["utype"] = tp
                    return HttpResponseRedirect("/temp/admin/")

                elif tp == "user":

                    request.session["uid"] = uid
                    request.session["utype"] = tp
                    return HttpResponseRedirect("/temp/users/")

                elif tp == "lawyer":

                    # Check lawyer approval status
                    lawyer = RegisterLawyer.objects.filter(
                        lawyer_id=uid
                    ).first()

                    if lawyer is None:
                        return _fail(request, "No lawyer profile was found for this account.", "noacct")

                    status = (lawyer.status or "").lower()

                    if status == "accepted":

                        request.session["uid"] = uid
                        request.session["utype"] = tp
                        return HttpResponseRedirect("/temp/lawyers/")

                    elif status == "rejected":
                        return _fail(request, "Your lawyer application has been rejected by the admin.", "rejected")

                    else:
                        return _fail(request, "Your lawyer application is still pending admin approval.", "pending")

        # 3. Username exists but the password did not match
        return _fail(request, "Incorrect password. Please try again.", "wrong")

    return render(request, "login/login.html")


def register(request):
    return render(request, "login/register.html")