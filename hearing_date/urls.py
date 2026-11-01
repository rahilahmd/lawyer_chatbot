from django.conf.urls import url
from hearing_date import views
urlpatterns = [
    url('hearing/',views.hearingdetails),
    url('view_H/',views.viewhearingdetails),
    url('update_H/(?P<idd>\w+)', views.updatehearingdetails),
]