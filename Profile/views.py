from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class ProfileView(LoginRequiredMixin, View):
    login_url='/authentication/login'

    def get(self, request):
        return render(request, 'profile/edit-profile.html')
    
    def post(self, request):
        return render(request, 'profile/edit-profile.html')
    