from django.conf.urls import url
from feedback_table import views
urlpatterns = [
    url('feedback_table',views.feedback_table),
    url('view_f',views.viewfeedback),

]