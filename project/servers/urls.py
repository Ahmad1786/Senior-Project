from django.urls import path
from . import views, htmx_views, swap_views

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
    path('assign-task/<int:task_id>', htmx_views.assign_task, name="assign_task"),
    path('leaderboard/', htmx_views.leaderboard, name='leaderboard'),
    path('invitation/<int:server_id>', htmx_views.invitation, name ="invitation"),
    path('join-server/', htmx_views.join_server, name ="join_server"),
    path('close-modal/', htmx_views.close_modal, name ="close_modal"),
    path('reload-window/', htmx_views.reload_window, name ="reload_window"),
    path('create/', htmx_views.create_server, name='create_server'),
    path('mark-as-complete/<int:task_id>', htmx_views.mark_as_complete, name="mark_as_complete"),
    path('mark-as-paid/<int:bill_id>', htmx_views.mark_as_paid, name="mark_as_paid"),
    path('delete-post/<str:post_type>/<int:post_id>', htmx_views.delete_post, name="delete_post"),
]

swap_routes = [
    path('swap-request/<int:task_id>', swap_views.swap_request, name ="swap_request"),
    path('manage-swap-request/<int:swap_request_id>', swap_views.manage_swap_request, name ="manage_swap_request"),
    path('create-swap-offer/<int:swap_request_id>', swap_views.create_swap_offer, name ="create_swap_offer"),    
    path('swap-offer/<int:task_id>', swap_views.swap_offer, name ="swap_offer"),
    path('accept-swap-offer/<int:offer_id>', swap_views.accept_swap_offer, name ="accept_swap_offer"),
    path('decline-swap-offer/<int:offer_id>', swap_views.decline_swap_offer, name ="decline_swap_offer"),
]

urlpatterns += htmx_routes
urlpatterns += swap_routes
