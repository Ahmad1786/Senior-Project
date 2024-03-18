from django.urls import path
from . import test_servers, views, htmx_views

app_name = "servers"
urlpatterns = [
    path('server/<int:server_id>', views.server_page, name="server_page"),
]

htmx_routes = [
    path('add-bill/<int:server_id>', htmx_views.add_bill, name="add_bill"),
    path('add-task/<int:server_id>', htmx_views.add_task, name="add_task"),
    path('add-event/<int:server_id>', htmx_views.add_event, name="add_event"),
]

urlpatterns += htmx_routes

test_routes = [
    path('server/test/<int:id>', test_servers.test_server, name="test_server"),
]

urlpatterns += test_routes