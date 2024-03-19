from django.urls import path
from . import test_users, views, feed_views

app_name = "users"
urlpatterns = [
    path('profile', views.profile, name="profile"), # a profile page for testing
    path('send-test-mail', views.send_test_mail, name="send_test_mail"),
    path('feed', feed_views.feed_view, name="feed_view"),
]

testing_routes = [
    path('user/<int:id>', test_users.test_user, name="test_user")
]

urlpatterns += testing_routes