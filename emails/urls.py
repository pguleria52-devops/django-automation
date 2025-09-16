from django.urls import path
from . import views

urlpatterns = [
    path('sent-email/', views.send_email, name='send_email'),
]