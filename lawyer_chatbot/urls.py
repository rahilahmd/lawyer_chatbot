"""lawyer_chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from temp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url('complaint/',include('complaint.urls')),
    url('feedback_table/',include('feedback_table.urls')),
    url('hearing_date/',include('hearing_date.urls')),
    url('login/',include('login.urls')),
    url('manage_appointment_and_fee/',include('manage_appointment_and_fee.urls')),
    url('near_by_policestation/',include('near_by_policestation.urls')),
    url('register_lawyer/',include('register_lawyer.urls')),
    url('user_register/',include('user_register.urls')),
    url('temp/',include('temp.urls')),
    url('chatbot/',include('chatbot.url')),
    url('$',views.home)


]
