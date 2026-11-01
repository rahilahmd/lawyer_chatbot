from django.conf.urls import url
from register_lawyer import views

urlpatterns = [
    url('register/', views.registerlawyer),
    url('view_prfl/', views.updateview),
    # url('update_prfl/', views.update),
    url('admin_viewpl/', views.manage),
    url('user_vie/', views.userview),
    url('accep/(?P<idd>\w+)', views.accept),
    url('rejec/(?P<idd>\w+)', views.reject),
    url('upda/(?P<idd>\w+)', views.update),
]