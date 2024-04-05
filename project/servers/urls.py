from django.urls import path
from . import test_servers, views, htmx_views, views2

app_name = "servers"
urlpatterns = [
    path('group-page/<int:server_id>', views.server_page, name="server_page"),
    path('join-server', views.join_server, name="join_server"),
    path('group-page2/<int:server_id>', views2.server_page, name="server_page2"),
]

htmx_routes = [
    path('add-bill/<int:server_id>', htmx_views.add_bill, name="add_bill"),
    path('edit-bill/<int:bill_id>', htmx_views.edit_bill, name= "edit_bill"),
    path('add-task/<int:server_id>', htmx_views.add_task, name="add_task"),
    path('edit-task/<int:task_id>', htmx_views.edit_task, name="edit_task"),
    path('add-event/<int:server_id>', htmx_views.add_event, name="add_event"),
    path('edit-event/<int:event_id>', htmx_views.edit_event, name ="edit_event"),
    path('assign-task/<int:task_id>', htmx_views.assign_task, name="assign_task"),
    path('invitation/<int:server_id>', htmx_views.invitation, name ="invitation"),
    path('join-server/', htmx_views.join_server, name ="join_server"),
    path('close-modal/', htmx_views.close_modal, name ="close_modal"),
]

urlpatterns += htmx_routes

test_routes = [
    path('test-server/<int:id>', test_servers.test_server, name="test_server"),
]

urlpatterns += test_routes
