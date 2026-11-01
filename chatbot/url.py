from django.conf.urls import url,include
from chatbot import views

urlpatterns = [
    url('chatbot/',views.chatbot)
]