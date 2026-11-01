from django.conf.urls import url
from near_by_policestation import views
urlpatterns = [
    url('near_by_policestation/',views.nearbypolicestation),
    url('view_nearbypolicestation/',views.viewpolicestation),

]