from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from social.views import  Inicio, PostEditView, PostDeleteView,AddLike,CommentCreateView,SearchUser, ProximamenteView

app_name ="social"
urlpatterns = [
    path('',Inicio.as_view(),name="inicio"),
    path('edit/<int:pk>/', PostEditView.as_view(), name="edit_post"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('like/<int:pk>/', AddLike.as_view(), name='add_like'),
    path('create_comment/<int:pk>/', CommentCreateView.as_view(), name='create_comment'),
    path('search/',SearchUser.as_view(),name="search"),
    path('proximamente/', ProximamenteView.as_view(), name='proximamente'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)