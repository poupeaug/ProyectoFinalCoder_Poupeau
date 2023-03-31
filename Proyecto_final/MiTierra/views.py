from django.shortcuts import render
from MiTierra.models import Propiedad, Profile, Mensaje
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    return render(request, "MiTierra/index.html")

def about(request):
    return render(request, "MiTierra/about.html")

class PropiedadList(ListView):
    model = Propiedad
    context_object_name = "propiedades"

class PropiedadMineList(LoginRequiredMixin, PropiedadList):
    
    def get_queryset(self):
        return Propiedad.objects.filter(propietario=self.request.user.id).all()


class PropiedadDetail(DetailView):
    model = Propiedad
    context_object_name = "propiedad"


class PropiedadUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Propiedad
    success_url = reverse_lazy("propiedad-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        propiedad_id =  self.kwargs.get("pk")
        return Propiedad.objects.filter(propietario=user_id, id=propiedad_id).exists()


class PropiedadDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Propiedad
    context_object_name = "propiedad"
    success_url = reverse_lazy("propiedad-list")

    def test_func(self):
        user_id = self.request.user.id
        propiedad_id =  self.kwargs.get("pk")
        return Propiedad.objects.filter(propietario=user_id, id=propiedad_id).exists()


class PropiedadCreate(LoginRequiredMixin, CreateView):
    model = Propiedad
    success_url = reverse_lazy("propiedad-list")
    fields = '__all__'


class PropiedadSearch(ListView):
    model = Propiedad
    context_object_name = "propiedades"

    def get_queryset(self):
        criterio = self.request.GET.get("criterio")
        result = Propiedad.objects.filter(nombre=criterio).all()
        return result

class Login(LoginView):
    next_page = reverse_lazy("propiedad-list")

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('propiedad-list')

class Logout(LogoutView):
    template_name = 'registration/logout.html'

class ProfileCreate(CreateView):
    model = Profile
    success_url = reverse_lazy("propiedad-list")
    fields = ['avatar']
    #para validar el usuario
    def form_valid(self, form):
        form.instance.User = self.request.user
        return super().form_valid(form)

class ProfileUpdate(UserPassesTestMixin, UpdateView):
    model = Profile
    success_url = reverse_lazy("propiedad-list")
    fields = ['avatar']
    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()

class MensajeCreate(CreateView):
    model = Mensaje
    success_url = reverse_lazy("mensaje-create")
    fields = "__all__"

class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    context_object_name = "mensaje"
    success_url = reverse_lazy("mensaje-list")
    def test_func(self):
        return Mensaje.objects.filter(destinatario=self.request.user).exists()
    
class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"
    def get_queryset(self):
        import pdb; pdb.set_trace
        return Mensaje.objects.filter(destinatario=self.request.user).all()





