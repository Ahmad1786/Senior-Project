from django.urls import path
from . import test_posts, views, htmx_views, recurring_task_views

app_name = "posts"
urlpatterns = [
    path('bill/<int:id>', views.bill, name="bill"),
    path('chore/<int:id>', views.chore, name="chore"),
    path('event/<int:id>', views.event, name="event"),
    path("add-reply/<str:post_type>/<int:post_id>/<int:parent_comment_id>", views.add_reply, name="add_reply"),
    path("edit-comment/<str:post_type>/<int:post_id>/<int:comment_id>", views.edit_comment, name="edit_comment"),
    path("delete-comment/<str:post_type>/<int:post_id>/<int:comment_id>", views.delete_comment, name="delete_comment"), 
    path("create-recurring-task/<int:server_id>", recurring_task_views.create_recurring_task, name="create_recurring_task"),
]

testing_routes = [
    path('test-bill/<int:id>', test_posts.test_bill, name="test_bill"),
    path('test-chore/<int:id>', test_posts.test_chore, name="test_chore"),
    path('test-event/<int:id>', test_posts.test_event, name="test_event"),
    path('test-comment/<int:id>', test_posts.test_comment, name="test_comment"),
]

htmx_routes = [
    path('add-comment/<int:post_id>', htmx_views.add_comment, name="add_comment"),
    path("comment-box/<str:post_type>/<int:post_id>", htmx_views.add_comment, name="add_comment"),
    path("comment-section/<str:post_type>/<int:post_id>", htmx_views.get_comment_section, name="comment_section"),
]


urlpatterns += testing_routes
urlpatterns += htmx_routes
