from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'index.html'

class LogOut(TemplateView):
    template_name = 'logout.html'

class AboutPage(TemplateView):
    template_name = 'about.html'
