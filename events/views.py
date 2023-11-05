from django.shortcuts import render, redirect
from django.views import View
from .forms import EventForm


class CreateEventView(View):
    template_name = 'pages/create_event.html'

    def get(self, request):
        form = EventForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  # Asigna el creador del evento como el usuario actual
            event.save()
            # Realiza cualquier lógica adicional, como notificar a los superusuarios.
            return redirect('social:inicio') 
        return render(request, 'pages/create_event.html', {'form': form})
