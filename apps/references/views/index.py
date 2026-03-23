from django.views.generic import TemplateView


class ReferencesIndexView(TemplateView):
    template_name = "references/index.html"
