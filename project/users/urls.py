from django.urls import path
from . import test_users, views

app_name = "users"
urlpatterns = [
    path('profile', views.profile, name="profile"), # a profile page for testing
    path('send-test-mail', views.send_test_mail, name="send_test_mail"),
]

testing_routes = [
    path('user/<int:id>', test_users.test_user, name="test_user")
]

urlpatterns += testing_routes