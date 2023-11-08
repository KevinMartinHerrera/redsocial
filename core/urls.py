from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from accounts.views import CustomSignupView
from allauth.account.views import LoginView, LogoutView, SignupView
from social.views import  Inicio, PostEditView, PostDeleteView,AddLike,CommentCreateView,SearchUser, ProximamenteView



# Configuración de URLs
urlpatterns = [
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls), 
    path('', include('social.urls')),
    path('accounts/', include('allauth.urls')),  # URLs de AllAuth para autenticación
    path('users/', include('accounts.urls')),
    path('events/', include('events.urls')),
]



# Configuración de URLs para servir archivos estáticos y medios en modo de depuración
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
