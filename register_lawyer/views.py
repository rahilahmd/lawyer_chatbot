from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from register_lawyer.models import RegisterLawyer
from login.models import Login

import os
import uuid
import traceback


# File storage
fs = FileSystemStorage()

REGISTER_TEMPLATE = 'register_lawyer/register_lawyer.html'
PROFILE_URL = '/register_lawyer/view_prfl/'        # the lawyer's own profile page (viewprofilelawyer.html)
ADMIN_LIST_URL = '/register_lawyer/admin_viewpl/'   # the admin's list of lawyers
MIN_AGE = 23


# ----------------------------------
# HELPERS
# ----------------------------------

def _password_problem(password):
    """Return a message if the password is too weak, otherwise None."""
    if len(password) < 12:
        return "Password must contain at least 12 characters."
    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase letter."
    if not any(c.islower() for c in password):
        return "Password must contain a lowercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain a number."
    if not any(not c.isalnum() for c in password):
        return "Password must contain a special character."
    return None


def _file_problem(f, allowed, max_mb, label):
    """Return a message if an uploaded file is not allowed, otherwise None."""
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in allowed:
        return label + " must be " + ", ".join(e.strip('.').upper() for e in allowed) + "."
    if f.size > max_mb * 1024 * 1024:
        return label + " must be smaller than " + str(max_mb) + " MB."
    return None


def _age_problem(age):
    """Return (age_as_int, message). The message is None when the age is fine."""
    try:
        age = int(age)
    except (ValueError, TypeError):
        return None, "Enter a valid age."
    if age < MIN_AGE or age > 100:
        return None, "Lawyers must be between " + str(MIN_AGE) + " and 100 years old."
    return age, None


# ----------------------------------
# LAWYER REGISTRATION
# ----------------------------------

def registerlawyer(request):

    if request.method == "POST":

        photo_path = None
        certificate_path = None

        def fail(message):
            messages.error(request, message)
            return render(request, REGISTER_TEMPLATE)

        try:
            full_name = request.POST.get('full_name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            address = request.POST.get('address')
            email = request.POST.get('email')
            user_name = request.POST.get('user_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            qualification = request.POST.get('lawyer_qualification')
            other_q = request.POST.get('other_qualification')

            lawyer_category = request.POST.get('lawyer_category')
            phone_number = request.POST.get('phone_number')

            # the registration form sends "enrollment_number"; older forms sent "bar_enrollment"
            bar_enrollment = request.POST.get('enrollment_number') or request.POST.get('bar_enrollment')

            photo = request.FILES.get('photo')
            certificate = request.FILES.get('certificate')

            # Required field validation
            if not all([
                full_name, age, gender, dob, address,
                email, user_name, password, qualification,
                lawyer_category, phone_number, bar_enrollment
            ]):
                return fail("Please fill all required fields.")

            # Password confirmation and strength
            if password != confirm_password:
                return fail("Passwords do not match.")

            problem = _password_problem(password)
            if problem:
                return fail(problem)

            # Duplicates
            if RegisterLawyer.objects.filter(email=email).exists():
                return fail("Email already registered.")

            if RegisterLawyer.objects.filter(user_name=user_name).exists() \
                    or Login.objects.filter(username=user_name).exists():
                return fail("Username already exists.")

            # Qualification
            if qualification == "Other":
                if not other_q:
                    return fail("Please enter your qualification.")
                qualification = other_q

            # Age validation (minimum 23)
            age, problem = _age_problem(age)
            if problem:
                return fail(problem)

            # Files
            if not photo or not certificate:
                return fail("Please upload your photo and certificate.")

            problem = _file_problem(photo, ['.jpg', '.jpeg', '.png'], 2, "Photo")
            if problem:
                return fail(problem)

            problem = _file_problem(certificate, ['.pdf', '.jpg', '.jpeg', '.png'], 5, "Certificate")
            if problem:
                return fail(problem)

            photo_ext = os.path.splitext(photo.name)[1].lower()
            certificate_ext = os.path.splitext(certificate.name)[1].lower()
            photo_name = 'lawyer_' + str(uuid.uuid4()) + photo_ext
            certificate_name = 'certificate_' + str(uuid.uuid4()) + certificate_ext

            # Hash password
            hashed_password = make_password(password)

            # Save lawyer and login details
            with transaction.atomic():

                obj = RegisterLawyer()

                obj.full_name = full_name
                obj.age = age
                obj.gender = gender
                obj.dob = dob
                obj.address = address
                obj.email = email
                obj.user_name = user_name
                obj.password = hashed_password

                obj.lawyer_qualification = qualification
                obj.lawyer_category = lawyer_category
                obj.phone_number = phone_number
                obj.bar_enrollment = bar_enrollment

                obj.status = 'Pending'

                # Save uploaded files
                photo_path = fs.save(photo_name, photo)
                certificate_path = fs.save(certificate_name, certificate)

                obj.photo = photo_path
                obj.certificate = certificate_path

                obj.save()

                # Create login account
                ob = Login()

                ob.username = user_name
                ob.password = hashed_password
                ob.type = 'lawyer'
                ob.uid = obj.lawyer_id

                ob.save()

            messages.success(
                request,
                "Registration successful! Your account is waiting for admin verification."
            )

            return redirect('/register_lawyer/register/')

        except Exception as e:

            # Show actual error in PyCharm terminal
            print("\n========== REGISTRATION ERROR ==========")
            print(str(e))
            traceback.print_exc()
            print("========================================\n")

            # Remove uploaded files if database saving failed
            for path in (photo_path, certificate_path):
                if path:
                    try:
                        fs.delete(path)
                    except Exception:
                        pass

            messages.error(
                request,
                "Registration failed. Check the PyCharm terminal for the actual error."
            )

    return render(request, REGISTER_TEMPLATE)


# ----------------------------------
# VIEW APPROVED LAWYERS
# ----------------------------------

def userview(request):

    obj = RegisterLawyer.objects.filter(status='accepted')

    context = {
        'uv': obj
    }

    return render(
        request,
        'register_lawyer/userview.html',
        context
    )


# ----------------------------------
# ADMIN MANAGE LAWYERS
# ----------------------------------

def manage(request):

    obj = RegisterLawyer.objects.all()

    context = {
        'rl': obj
    }

    return render(
        request,
        'register_lawyer/viewlawyerprofile.html',
        context
    )


# ----------------------------------
# ACCEPT LAWYER
# ----------------------------------

def accept(request, idd):

    obj = RegisterLawyer.objects.get(lawyer_id=idd)

    obj.status = 'accepted'
    obj.save()

    messages.success(request, "Lawyer approved successfully.")

    return redirect(ADMIN_LIST_URL)


# ----------------------------------
# REJECT LAWYER
# ----------------------------------

def reject(request, idd):

    obj = RegisterLawyer.objects.get(lawyer_id=idd)

    obj.status = 'rejected'
    obj.save()

    messages.success(request, "Lawyer rejected.")

    return redirect(ADMIN_LIST_URL)


# ----------------------------------
# UPDATE LAWYER PROFILE
# ----------------------------------

def update(request, idd):

    uid = request.session.get('uid')
    utype = request.session.get('utype')      # set in the login view: 'admin', 'user' or 'lawyer'

    # must be logged in
    if not uid:
        return redirect('/login/')

    # normal users may not open this page
    if utype not in (None, 'admin', 'lawyer'):
        return redirect('/login/')

    # a lawyer edits their own profile and returns to it; the admin returns to the lawyer list
    is_lawyer = (utype == 'lawyer') or (utype is None and str(uid) == str(idd))

    if is_lawyer and str(uid) != str(idd):
        return redirect(PROFILE_URL)           # a lawyer cannot edit someone else's profile

    back_url = PROFILE_URL if is_lawyer else ADMIN_LIST_URL
    edit_url = '/register_lawyer/upda/' + str(idd)

    obj = get_object_or_404(RegisterLawyer, lawyer_id=idd)

    if request.method == "POST":

        def fail(message):
            messages.error(request, message)
            return redirect(edit_url)

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        category = request.POST.get('lawyer_category')
        new_user_name = (request.POST.get('user_name') or '').strip()
        new_password = request.POST.get('password') or ''

        # Age (minimum 23)
        age, problem = _age_problem(request.POST.get('age'))
        if problem:
            return fail(problem)

        # Qualification ("Other" uses the text the lawyer typed)
        qualification = request.POST.get('lawyer_qualification')
        if qualification == "Other":
            other_q = (request.POST.get('other_qualification') or '').strip()
            if not other_q:
                return fail("Please enter your qualification.")
            qualification = other_q

        # Email must stay unique
        if RegisterLawyer.objects.filter(email=email).exclude(lawyer_id=idd).exists():
            return fail("Email already registered.")

        # Username must stay unique
        if new_user_name and new_user_name != obj.user_name:
            if RegisterLawyer.objects.filter(user_name=new_user_name).exclude(lawyer_id=idd).exists() \
                    or Login.objects.filter(username=new_user_name).exists():
                return fail("Username already exists.")

        # Password changes only when a new one is typed
        if new_password:
            problem = _password_problem(new_password)
            if problem:
                return fail(problem)

        # Files
        photo = request.FILES.get('photo')
        certificate = request.FILES.get('certificate')

        if photo:
            problem = _file_problem(photo, ['.jpg', '.jpeg', '.png'], 2, "Photo")
            if problem:
                return fail(problem)

        if certificate:
            problem = _file_problem(certificate, ['.pdf', '.jpg', '.jpeg', '.png'], 5, "Certificate")
            if problem:
                return fail(problem)

        # Everything is valid: save
        with transaction.atomic():

            obj.full_name = full_name
            obj.age = age
            obj.gender = gender
            obj.dob = dob
            obj.address = address
            obj.email = email
            obj.phone_number = phone_number
            obj.lawyer_qualification = qualification
            obj.lawyer_category = category

            if photo:
                photo_ext = os.path.splitext(photo.name)[1].lower()
                obj.photo = fs.save('lawyer_' + str(uuid.uuid4()) + photo_ext, photo)

            if certificate:
                certificate_ext = os.path.splitext(certificate.name)[1].lower()
                obj.certificate = fs.save('certificate_' + str(uuid.uuid4()) + certificate_ext, certificate)

            # keep the login account in step with the profile
            login_row = Login.objects.filter(uid=idd, type='lawyer').first()

            if new_user_name:
                obj.user_name = new_user_name
                if login_row:
                    login_row.username = new_user_name

            if new_password:
                hashed = make_password(new_password)
                obj.password = hashed
                if login_row:
                    login_row.password = hashed

            obj.save()
            if login_row:
                login_row.save()

        messages.success(request, "Profile updated successfully.")

        return redirect(back_url)

    context = {
        'j': obj
    }

    return render(
        request,
        'register_lawyer/updateprofile.html',
        context
    )


# ----------------------------------
# LAWYER VIEW OWN PROFILE
# ----------------------------------

def updateview(request):

    ss = request.session.get('uid')

    if not ss:
        return redirect('/login/')

    obj = RegisterLawyer.objects.filter(lawyer_id=ss)

    context = {
        'uv': obj
    }

    return render(
        request,
        'register_lawyer/viewprofilelawyer.html',
        context
    )