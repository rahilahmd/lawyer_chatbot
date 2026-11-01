from django.conf.urls import url
from temp import views
urlpatterns = [
    url('home/', views.home),
    url('lawyers/', views.lawyers),
    url('admin/', views.admin),
    url('users/', views.users),

]