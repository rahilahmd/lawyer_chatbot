from django.conf.urls import url
from user_register import views

urlpatterns = [
    url('register/', views.userregister),
    url('view_u/', views.viewuserdetails),
]
