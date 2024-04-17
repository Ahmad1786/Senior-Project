from django.urls import path
from . import test_servers, views, htmx_views

app_name = "servers"
urlpatterns = [
    path('group-page/<int:server_id>', views.server_page, name="server_page"),
    path('join-server', views.join_server, name="join_server"),
]

htmx_routes = [
    path('add-bill/<int:server_id>', htmx_views.add_bill, name="add_bill"),
    path('edit-bill/<int:bill_id>', htmx_views.edit_bill, name= "edit_bill"),
    path('add-task/<int:server_id>', htmx_views.add_task, name="add_task"),
    path('edit-task/<int:task_id>', htmx_views.edit_task, name="edit_task"),
    path('add-event/<int:server_id>', htmx_views.add_event, name="add_event"),
    path('edit-event/<int:event_id>', htmx_views.edit_event, name ="edit_event"),
    path('assign-task/', htmx_views.assign_task, name="assign_task"),
    path('invitation/<int:server_id>', htmx_views.invitation, name ="invitation"),
    path('join-server/', htmx_views.join_server, name ="join_server"),
    path('swap-request/<int:task_id>', htmx_views.swap_request, name ="swap_request"),
    path('manage-swap-request/<int:swap_request_id>', htmx_views.manage_swap_request, name ="manage_swap_request"),
    path('create-swap-offer/<int:swap_request_id>', htmx_views.create_swap_offer, name ="create_swap_offer"),    
    path('swap-offer/<int:task_id>', htmx_views.swap_offer, name ="swap_offer"),
    path('accept-swap-offer/<int:offer_id>', htmx_views.accept_swap_offer, name ="accept_swap_offer"),
    path('decline-swap-offer/<int:offer_id>', htmx_views.decline_swap_offer, name ="decline_swap__offer"),
    path('close-modal/', htmx_views.close_modal, name ="close_modal"),
    path('reload-window/', htmx_views.reload_window, name ="reload_window"),
]

urlpatterns += htmx_routes

test_routes = [
    path('test-server/<int:id>', test_servers.test_server, name="test_server"),
]

urlpatterns += test_routes
