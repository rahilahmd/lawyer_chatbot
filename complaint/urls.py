from django.conf.urls import url
from complaint import views
urlpatterns = [
    url('complaint/',views.complaints),
    url('post_rep/(?P<idd>\w+)',views.postcomplaintreplay),
    url('vie_com/',views.viewcomplaints),
    url('rep_com/',views.replaycomplaints),
    url('rp_view/',views.replyview),
    url('repl/(?P<idd>\w+)', views.postcomplaintreplay),
]
