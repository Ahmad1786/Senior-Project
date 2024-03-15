from django.urls import path
from . import test_posts, views, supply_board_views

app_name = "posts"
urlpatterns = [
    
]

testing_routes = [
    path('bill/<int:id>', test_posts.test_bill, name="test_bill"),
    path('chore/<int:id>', test_posts.test_chore, name="test_chore"),
    path('event/<int:id>', test_posts.test_event, name="test_event"),
    path('comment/<int:id>', test_posts.test_comment, name="test_comment"),
]

# temporary list until merge all the group page routes
group_page_routes = [
    path('supply-board/<int:server_id>', supply_board_views.supply_board, name="supply_board"),
]

htmx_routes = [
    path('add-bill/<int:server_id>', supply_board_views.add_bill, name="add_bill"),
]



urlpatterns += testing_routes
urlpatterns += htmx_routes
urlpatterns += group_page_routes
