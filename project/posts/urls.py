from django.urls import path
from . import test_posts, views

app_name = "posts"
urlpatterns = []

   
testing_routes = [
    path('bill/<int:id>', test_posts.test_bill, name="test_bill"),
    path('chore/<int:id>', test_posts.test_chore, name="test_chore"),
    path('event/<int:id>', test_posts.test_event, name="test_event"),
    path('comment/<int:id>', test_posts.test_comment, name="test_comment"),
]

htmx_routes = []


urlpatterns += testing_routes
urlpatterns += htmx_routes
