from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    def get_success_url(self):
        return reverse_lazy('jobs:create')
    template_name = 'accounts/signup.html'
