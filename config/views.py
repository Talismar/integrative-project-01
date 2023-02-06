from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import TemplateView

def index(request):
    return render(request, 'index.html')

class Redirection(View):
    def get(self, request, *args, **kwargs):

        if request.user.groups.filter(name="Admin").exists():
            return redirect('clinic:home')

        elif request.user.groups.filter(name="Employee").exists():
            return redirect('clinic:home')

        else: # Patient
            return redirect('patient:home')

class AboutPageView(TemplateView):
    template_name = 'pages/sobre.html'
    extra_context = {
        "about": True
    }
