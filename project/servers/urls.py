from django.urls import path
from . import test_servers, views

app_name = "servers"
urlpatterns = [
    
]

test_routes = [
    path('server/<int:id>', test_servers.test_server, name="test_server"),
]

urlpatterns += test_routes