from django.urls import path
from .views import CreateEventView

app_name ="events"
urlpatterns = [
    # Otras rutas de tu aplicación
    path('create/', CreateEventView.as_view(), name='create_event'),
]