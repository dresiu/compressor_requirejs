
from django.template import Template, Context
from django.conf import settings

from compressor.filters import FilterBase


class TemplateFilter(FilterBase):
    def input(self, filename=None, basename=None, **kwargs):
        template = Template(self.content)
        js_variables = {}

        js_variables.update({'STATIC_URL': settings.STATIC_URL})
        js_variables.update({'JSON_OBJECT': {
            'var1': 'something',
            'var2': 'something2'
        }})
        context = Context(js_variables)
        return template.render(context)
