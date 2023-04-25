from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
User = get_user_model()

from . forms import RegisterForm, UpdateUserForm


class UserRegistration(FormView):
    template_name = 'user/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')

    def form_valid(self, form):
        form.save()
        return super(UserRegistration, self).form_valid(form)

class UserDetailView(DetailView):
    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'

class UpdateUserView(SuccessMessageMixin,UpdateView):
    model = User
    template_name = 'user/update_user.html'
    form_class = UpdateUserForm
    success_message = 'Perfil actualizado exitosamente!!!'
    
    def get_success_url(self):
        return reverse_lazy('users:user', args=[self.object.id])

    
