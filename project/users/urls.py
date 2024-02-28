from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('profile', views.profile, name="profile"), # a profile page for testing
    path('send-test-mail', views.send_test_mail, name="send_test_mail"),
]