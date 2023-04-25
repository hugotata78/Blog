from django.urls import path
from django.views.generic import TemplateView

from User import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('success/', TemplateView.as_view(template_name='user/success_registration.html'), name='success'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user'),
    path('user/update/<int:pk>', views.UpdateUserView.as_view(), name='update'),
]