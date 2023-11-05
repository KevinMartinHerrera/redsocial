from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from .views import UserProfileView
from . import views


app_name ="accounts"

urlpatterns = [
    path("<username>", UserProfileView.as_view(), name="profile"),
    
    path('send_friend_request/<int:to_user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/', views.manage_friend_requests, name='friend_requests'),
    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
