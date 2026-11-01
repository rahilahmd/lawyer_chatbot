from django.urls import path
from . import views

urlpatterns = [

    path('book_appointment/<int:idd>/', views.appointmentandfees, name='book_appointment'),

    path('adminview/', views.adminviewapp, name='adminview'),

    path('appviewuser/', views.appviewuser, name='appviewuser'),

    path('view_ap/', views.viewappointment, name='view_ap'),

    path('accep/<int:idd>/', views.accept, name='accept'),

    path('rejec/<int:idd>/', views.reject, name='reject'),

    path('del/<int:idd>/', views.deleteappointment, name='deleteappointment'),

]