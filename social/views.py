from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from .models import Facultad, Image, SocialPost
from accounts.models import Profile,FriendRequest,User
from events.models import Event
from social.forms import Socialpostforms, SocialCommentsForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
    
from django.db.models import Q

class Inicio(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page')
        posts_per_page = 10
        events = Event.objects.filter(accepted=True)

        form = Socialpostforms()
        CommentForm = SocialCommentsForm()
        facultades = Facultad.objects.all()
        

        if request.user.is_authenticated:
            logged_in_user = request.user
            friend_requests_sent = FriendRequest.objects.filter(from_user=logged_in_user, accepted=True)
            friend_requests_received = FriendRequest.objects.filter(to_user=logged_in_user, accepted=True)
            
            amigos = [friend_request.to_user if friend_request.from_user == logged_in_user else friend_request.from_user for friend_request in friend_requests_sent] + \
                     [friend_request.from_user if friend_request.to_user == logged_in_user else friend_request.to_user for friend_request in friend_requests_received]
            
            posts = SocialPost.objects.filter(Q(author=logged_in_user) | Q(author__in=amigos)).prefetch_related('comments')
            
            paginator = Paginator(posts, posts_per_page)
            users = User.objects.exclude(id=logged_in_user.id).exclude(id__in=[amigo.id for amigo in amigos])

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
        else:
            posts = SocialPost.objects.prefetch_related('comments').all()

        context = {
            'facultades': facultades,
            'form': form,
            'posts': posts,
            'CommentForm': CommentForm,
            'amigos': amigos if request.user.is_authenticated else [],
            'events': events,
            'users':users if request.user.is_authenticated else []
        }

        return render(request, 'pages/index.html', context)

        
    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        form = Socialpostforms(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        posts = SocialPost.objects.all()
 

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = logged_in_user
            new_post.save()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

            # Crear un nuevo formulario vacío para mostrar en la plantilla
            form = Socialpostforms()

        CommentForm = SocialCommentsForm()  # Define CommentForm antes de verificar su validez

        facultades = Facultad.objects.all()
        posts = SocialPost.objects.all()

        context = {
            'facultades': facultades,
            'form': form,
            'posts': posts,
            'CommentForm': CommentForm,
        }
        
        return redirect(request.path)
    
class CommentCreateView(View):
    def post(self, request, pk, *args, **kwargs):
        logged_in_user = request.user
        CommentForm = SocialCommentsForm(request.POST)

        if CommentForm.is_valid():
            new_comment = CommentForm.save(commit=False)
            new_comment.author = logged_in_user
            new_comment.post = SocialPost.objects.get(pk=pk)
            new_comment.save()

            # Incluye los datos del comentario en la respuesta JSON
            comment_data = {
                'author_profile_url': new_comment.author.profile.foto_de_perfil.url,
                'author_username': new_comment.author.username,
                'comment': new_comment.comment,
                'created_on': new_comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            }

            return JsonResponse({'success': True, 'comment': comment_data})
        else:
            return JsonResponse({'success': False, 'message': 'Error en la validación del comentario'})
    
class PostEditView(UpdateView):
    model = SocialPost
    fields = ['body']
    template_name = 'social/editar_publicacion_modal.html'  # Asegúrate de que esto apunte a tu plantilla de edición
    success_url = reverse_lazy('social:inicio')

class PostDeleteView(DeleteView):
    model = SocialPost
    template_name = 'social/delete_post_confirm.html'  # Crea esta plantilla
    success_url = reverse_lazy('social:inicio')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Verificar si el usuario autenticado es el autor de la publicación
        if self.object.author == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            # Redirigir a alguna página de error o mostrar un mensaje
            # Puedes personalizar esto según tus necesidades.
            return HttpResponse("No tienes permiso para eliminar esta publicación.")

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        user = request.user
        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(user)
        
        is_like = False
        for like in post.likes.all():
            if like == user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(user)
        if is_like:
            post.likes.remove(user)

        return JsonResponse({'is_like': is_like, 'likes_count': post.likes.count()})

from django.db.models import Q

      
class SearchUser(View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        query = self.request.GET.get('query')
        facultades = Facultad.objects.all()
        profile_list = Profile.objects.filter(Q(user__username__icontains=query))
        
        for profile in profile_list:
            pending_request = FriendRequest.objects.filter(
                from_user=logged_in_user,
                to_user=profile.user
            )
            if pending_request.exists():
                profile.friend_request_status = 'pending'
            else:
                profile.friend_request_status = 'not_sent'

        friend_requests_sent = FriendRequest.objects.filter(from_user=logged_in_user, accepted=True)
        friend_requests_received = FriendRequest.objects.filter(to_user=logged_in_user, accepted=True)

        # Obtiene a los usuarios amigos basados en las solicitudes aceptadas
        amigos = [friend_request.to_user if friend_request.from_user == logged_in_user else friend_request.from_user for friend_request in friend_requests_sent] + \
             [friend_request.from_user if friend_request.to_user == logged_in_user else friend_request.to_user for friend_request in friend_requests_received]

        context = {
            'facultades': facultades,
            'profile_list': profile_list,
            'amigos': amigos
        }
        return render(request, 'pages/search.html', context)


class ProximamenteView(View):
    def get(self, request):
        return render(request, 'pages/proximamente.html')
    
