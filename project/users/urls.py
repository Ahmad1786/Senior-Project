from django.urls import path
from . import notification_views, views, feed_views, profile_pic_view

app_name = "users"
urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('send-test-mail', views.send_test_mail, name="send_test_mail"),
    path('feed', feed_views.feed_view, name="feed_view"),
    path('upload-profile-pic', profile_pic_view.profile_pic, name="profile_pic"),
    path('notifications', notification_views.notification_page, name="notification_page"),
    path('unread-notification-count', notification_views.unread_notification_count, name="unread_notification_count"),
    path('mark-as-read/<int:notification_id>', notification_views.mark_as_read, name="mark_as_read"),
    path('edit-phone-number', views.edit_phone_number, name="edit_phone_number"),
    path('empty', views.empty_response, name="empty_response"),
]