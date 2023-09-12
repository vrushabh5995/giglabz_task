from django.urls import path
from .views import *

urlpatterns = [
    path("api/addUser", addUser),
    path("api/login", LoginAPIView.as_view()),
    path("api/Logout", LogoutAPIView.as_view()),
    path("api/timeconverter/", TimeconverterView.as_view()),
    path("api/users", UserViewSet.as_view({'get': 'list'})),
    path("api/update", UpdateUserViewSet.as_view({'get': 'update'})),
    
]