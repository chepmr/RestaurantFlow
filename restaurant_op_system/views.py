from django.views.generic import TemplateView

from project_apps.reservations.models import Table


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.filter(in_service=True).order_by('number')[:6]

        return context