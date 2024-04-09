from django.urls import path
from . import notification_views, test_users, views, feed_views, profile_pic_view

app_name = "users"
urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('send-test-mail', views.send_test_mail, name="send_test_mail"),
    path('feed', feed_views.feed_view, name="feed_view"),
    path('upload-profile-pic', profile_pic_view.profile_pic, name="profile_pic"),
    path('notifications', notification_views.notification_page, name="notification_page"),
    path('unread-notification-count', notification_views.unread_notification_count, name="unread_notification_count"),
    path('mark-as-read/<int:notification_id>', notification_views.mark_as_read, name="mark_as_read"),
]

testing_routes = [
    path('user/<int:id>', test_users.test_user, name="test_user")
]

urlpatterns += testing_routes