from django.urls import path
from . import test_posts, views, htmx_views

app_name = "posts"
urlpatterns = [
    path('bill/<int:id>', views.bill, name="bill"),
    path('chore/<int:id>', views.chore, name="chore"),
    path('event/<int:id>', views.event, name="event"),
    path("add-reply/<int:id>", views.add_reply, name="add_reply")
]

testing_routes = [
    path('test-bill/<int:id>', test_posts.test_bill, name="test_bill"),
    path('test-chore/<int:id>', test_posts.test_chore, name="test_chore"),
    path('test-event/<int:id>', test_posts.test_event, name="test_event"),
    path('test-comment/<int:id>', test_posts.test_comment, name="test_comment"),
]

htmx_routes = [
    path('add-comment/<int:post_id>', htmx_views.add_comment, name="add_comment"),
]


urlpatterns += testing_routes
urlpatterns += htmx_routes
