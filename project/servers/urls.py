from django.urls import path
from . import test_servers, views, htmx_views

app_name = "servers"
urlpatterns = [
    path('server/<int:server_id>', views.server_page, name="server_page"),
]

htmx_routes = [
    path('add-bill/<int:server_id>', htmx_views.add_bill, name="add_bill"),
    path('edit-bill/<int:bill_id>', htmx_views.edit_bill, name= "edit_bill"),
    path('add-task/<int:server_id>', htmx_views.add_task, name="add_task"),
    path('edit-task/<int:task_id>', htmx_views.edit_task, name="edit_task"),
    path('add-event/<int:server_id>', htmx_views.add_event, name="add_event"),
    path('edit-event/<int:event_id>', htmx_views.edit_event, name ="edit_event"),
    path('join-server', htmx_views.join_server, name="join_server")
]

urlpatterns += htmx_routes

test_routes = [
    path('test-server/<int:id>', test_servers.test_server, name="test_server"),
]

urlpatterns += test_routes
