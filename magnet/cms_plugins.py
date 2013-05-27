__author__ = 'djakson'
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from models import MagnetPlugin as MagnetPluginModel, Magnet, Order, get_order, MagnetImage
from django.forms import ModelForm

class MagnetForm(ModelForm):
    class Meta:
        model = MagnetPluginModel

class HelloPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Hello Plugin")
    render_template = "hello_plugin.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(HelloPlugin)



def get_random_magnet():
    import random, math
    count = MagnetImage.objects.all().count()
    slc = int(math.floor(random.random() * count))
    magnets = MagnetImage.objects.all()[slc:slc+1]
    if magnets:
        return magnets[0]

class MagnetPlugin(CMSPluginBase):
    model = MagnetPluginModel
    name = _('Magnet')
    render_template = 'magnet.html'

    def render(self, context, instance, placeholder):
        from imagnet import settings
        context['instance'] = instance
        context['form'] = MagnetForm()
        context['uploadcare'] = settings.UPLOADCARE
        context['random_magnet'] = get_random_magnet()
        return context

plugin_pool.register_plugin(MagnetPlugin)


class MagnetListPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Magnet List')
    render_template = 'magnet_list.html'

    def render(self, context, instance, placeholder):
        request = context['request']
        context['order'] = get_order(request)
        return context

plugin_pool.register_plugin(MagnetListPlugin)