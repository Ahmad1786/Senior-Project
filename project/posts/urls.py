from django.urls import path
from . import test_posts, views

app_name = "posts"
urlpatterns = []

   
testing_routes = [
    path('test-bill/<int:id>', test_posts.test_bill, name="test_bill"),
    path('test-chore/<int:id>', test_posts.test_chore, name="test_chore"),
    path('test-event/<int:id>', test_posts.test_event, name="test_event"),
    path('test-comment/<int:id>', test_posts.test_comment, name="test_comment"),
    path('bill/<int:id>', views.bill, name="bill"),
    path('chore/<int:id>', views.chore, name="chore"),
    path('event/<int:id>', views.event, name="event"),
    path('comment/<int:id>', views.comment, name="comment")
]

htmx_routes = []


urlpatterns += testing_routes
urlpatterns += htmx_routes
