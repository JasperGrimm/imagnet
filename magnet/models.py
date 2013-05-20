# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pyuploadcare.dj import ImageField, ImageGroupField
from cms.models.pluginmodel import CMSPlugin
from datetime import datetime
from hashlib import md5
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _, string_concat


def get_image_size():
    return "768x768 upscale"

def new_order(request):
    order = Order()
    order.create_order_num()
    order.save()
    request.session['order_num'] = order.number
    return order

def get_order(request):
    order = request.session.get('order_num', False)
    if order:
        try:
            order = Order.objects.get(number=order)
        except ObjectDoesNotExist:
            order = new_order(request)
        return order
    else:
        order = new_order(request)
        return order

def get_order_statuses():
    return (('new',_('New order')), ('waiting_for_payment', _('Waiting for payment')), ('waiting_to_be_sent', _('Waiting to be sent')), ('sent', _('Sent')), ('canceled', _('Canceled')))

def get_payment_types():
    return (('online', _('Payment online')), ('after_delivery', _('After delivery')))

class MagnetPlugin(CMSPlugin):
    image = ImageField(null=True, blank=True, manual_crop=get_image_size())

class Magnet(models.Model):
    image = ImageField(null=True, blank=True, manual_crop=get_image_size(), verbose_name=_('Magnet image'))

    def __unicode__(self):
        return _('Magnet #%d') % self.pk

    class Meta:
        verbose_name = _('Magnet for the customer')
        verbose_name_plural = _('Magnets for the customers')

class Order(models.Model):
    number = models.CharField(max_length=200, verbose_name=_('Unique number of order (it\'s a part of the url)'))
    magnets = models.ManyToManyField(Magnet, related_name='order', verbose_name=_('Magnets'))
    status = models.CharField(choices=get_order_statuses(), max_length=200, verbose_name=_('Status'))

    fio = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    new_poshta_affiliate = models.CharField(max_length=10, blank=True, null=True)
    payment_type = models.CharField(max_length=200, choices=get_payment_types(), default=get_payment_types()[0])

    def create_order_num(self):
        self.number = get_random_string(10,allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789') + \
                      md5(str(datetime.now())).hexdigest()


    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class MagnetImage(models.Model):
    image = ImageField(verbose_name=_('Magnet image'), manual_crop=get_image_size())

    def __unicode__(self):
        return _('Magnet #%d') % self.pk

    class Meta:
        verbose_name = _('Image for magnet on main page')
        verbose_name_plural = _('Images for magnet on main page')

