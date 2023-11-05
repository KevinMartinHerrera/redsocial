from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import Profile
from social.models import Facultad,SocialPost
from django.contrib.auth import get_user_model
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import FriendRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse



def send_friend_request(request, to_user_id):
    # Obtener el destinatario de la solicitud
    to_user = User.objects.get(id=to_user_id)

    # Comprobar si ya existe una solicitud pendiente entre los usuarios
    existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user)

    # Verificar si los usuarios ya son amigos
    are_friends = FriendRequest.objects.filter(
        Q(from_user=request.user, to_user=to_user, accepted=True) |
        Q(from_user=to_user, to_user=request.user, accepted=True)
    ).exists()

    if not are_friends:
        if not existing_request:
            # Crear una nueva solicitud de amistad
            friend_request = FriendRequest(from_user=request.user, to_user=to_user)
            friend_request.save()

            response_data = {'message': 'Solicitud de amistad enviada con éxito.'}
        else:
            response_data = {'message': 'Ya existe una solicitud pendiente de amistad entre estos usuarios.'}
    else:
        response_data = {'message': 'Los usuarios ya son amigos.'}

    return JsonResponse(response_data)

    

def manage_friend_requests(request):
    # Obtener las solicitudes entrantes del usuario actual
    incoming_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    return render(request, 'pages/friend_requests.html', {'incoming_requests': incoming_requests})


def accept_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)

        if friend_request.to_user == request.user:
            friend_request.accepted = True
            friend_request.save()

            return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def reject_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)

        if friend_request.to_user == request.user:
            friend_request.delete()

            return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


User=get_user_model() 

class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        facultades = Facultad.objects.all()
        user_posts = SocialPost.objects.filter(author=user)
        
        profile_form = ProfileForm(profile=profile)
         # Obtén todas las solicitudes de amistad aceptadas
        friend_requests_sent = FriendRequest.objects.filter(from_user=user, accepted=True)
        friend_requests_received = FriendRequest.objects.filter(to_user=user, accepted=True)
    
    # Obtiene a los usuarios amigos basados en las solicitudes aceptadas
        amigos = [friend_request.to_user if friend_request.from_user == user else friend_request.from_user for friend_request in friend_requests_sent] + \
             [friend_request.from_user if friend_request.to_user == user else friend_request.to_user for friend_request in friend_requests_received]
        
        context = {
            'user': user,
            'profile': profile,
            'facultades': facultades,
            'profile_form': profile_form,
            'user_posts': user_posts,
            'amigos': amigos
        }
        return render(request, 'pages/profile.html', context)
        
    def post(self, request, username, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        facultades = Facultad.objects.all()
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil. Por favor, verifica los campos.')
        
        # Incluso si el formulario no es válido, lo pasamos al contexto
        context = {
            'user': user,
            'profile': profile,
            'facultades': facultades,
            'profile_form': profile_form  # Pasa el formulario al contexto
        }
        
        return redirect(request.path,context)

from allauth.account.views import SignupView
from .forms import CustomSignupForm  # Asegúrate de importar tu formulario personalizado

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'  # Cambia esto a tu propio archivo de plantilla
    form_class = CustomSignupForm