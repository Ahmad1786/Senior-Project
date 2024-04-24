from django.urls import path
from . import views, htmx_views, recurring_task_views

app_name = "posts"
urlpatterns = [
    path('bill/<int:id>', views.bill, name="bill"),
    path('chore/<int:id>', views.chore, name="chore"),
    path('event/<int:id>', views.event, name="event"),
    path("create-recurring-task/<int:server_id>", recurring_task_views.create_recurring_task, name="create_recurring_task"),
    path('chore-pic/<int:post_id>', views.chore_pic, name="chore_pic"),
]

htmx_routes = [
    path('add-comment/<int:post_id>', htmx_views.add_comment, name="add_comment"),
    path("add-reply/<str:post_type>/<int:post_id>/<int:parent_comment_id>/<str:replying_to>", htmx_views.add_reply, name="add_reply"),
    path("edit-comment/<str:post_type>/<int:post_id>/<int:comment_id>", htmx_views.edit_comment, name="edit_comment"),
    path("delete-comment/<str:post_type>/<int:post_id>/<int:comment_id>", htmx_views.delete_comment, name="delete_comment"), 
    path("comment-box/<str:post_type>/<int:post_id>", htmx_views.add_comment, name="add_comment"),
    path("comment-section/<str:post_type>/<int:post_id>", htmx_views.get_comment_section, name="comment_section"),
]


urlpatterns += htmx_routes
