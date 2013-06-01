# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from pyuploadcare.dj import ImageField, ImageGroupField
from cms.models.pluginmodel import CMSPlugin
from datetime import datetime
from hashlib import md5
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _, string_concat


def get_image_size():
    return "768x768 upscale"


def new_order(request, draft=False):
    if draft:
        order = OrderDraft()
    else:
        order = Order()
    order.create_order_num()
    order.status = 'new'
    order.save()
    request.session['order_num'] = order.number
    return order


def get_order(request, draft=False):
    order = request.session.get('order_num', False)
    if order:
        try:
            if draft:
                order = OrderDraft.objects.get(number=order)
            else:
                order = Order.objects.get(number=order)
        except ObjectDoesNotExist:
            order = new_order(request, draft)
        return order
    else:
        order = new_order(request, draft)
        return order


def get_order_statuses():
    return ('new', _('New order')), ('waiting_for_payment', _('Waiting for payment')), (
        'waiting_to_be_sent', _('Waiting to be sent')), ('sent', _('Sent')), ('canceled', _('Canceled'))


def get_payment_types():
    return ('online', _('Payment online')), ('after_delivery', _('After delivery'))


class MagnetPlugin(CMSPlugin):
    image = ImageField(null=True, blank=True, manual_crop=get_image_size())


class Magnet(models.Model):
    image = ImageField(null=True, blank=True, manual_crop=get_image_size(), verbose_name=_('Magnet image'))

    def __unicode__(self):
        return _('Magnet #%d') % self.pk

    class Meta:
        verbose_name = _('Magnet for the customer')
        verbose_name_plural = _('Magnets for the customers')


class Prices(models.Model):
    min_count = models.IntegerField(max_length=1000, default=0, verbose_name=_('count from'))
    max_count = models.IntegerField(max_length=1000, default=0, verbose_name=_('count to'))
    magent_price = models.DecimalField(max_length=10000, max_digits=100000, decimal_places=2, verbose_name=_('Price'))
    cash_on_delivery = models.DecimalField(max_length=10000, max_digits=100000, decimal_places=2,
                                           verbose_name=_('Cash on delivery'))
    cost_of_delivery = models.DecimalField(max_length=10000, max_digits=100000, decimal_places=2,
                                           verbose_name=_('Cost of delivery'))

    def __unicode__(self):
        out = ''
        if self.min_count == 0 and self.max_count > 0:
            out = _('less then %d') % self.max_count
        elif self.max_count == 0 and self.min_count > 0:
            out = _('more then %d') % self.min_count
        else:
            out = _('from %(from)f to %(to)f') % (self.min_count, self.max_count)
        return out

    class Meta:
        verbose_name = _('Magnet price')
        verbose_name_plural = _('Magnet prices')


class OrderDraft(models.Model):
    number = models.CharField(max_length=200, verbose_name=_('Unique number of order (it\'s a part of the url)'))
    magnets = models.ManyToManyField(Magnet, related_name='order_draft', verbose_name=_('Magnets'))

    def create_order_num(self):
        self.number = get_random_string(10, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789') + md5(
            str(datetime.now())
        ).hexdigest()

    def get_count(self):
        return self.magnets.count()

    def get_price(self):
        count = self.get_count()
        price = Prices.objects.filter(Q(min_count__lte=count), Q(Q(max_count__gt=count) | Q(max_count=0)))
        if price:
            return price[0]
        return None

    def get_total_sum(self):
        count = self.get_count()
        price = self.get_price()
        if price:
            return price.magent_price * count
        return 0

    def get_total_sum_with_delivery(self):
        count = self.get_count()
        price = self.get_price()
        if price:
            _sum = price.magent_price * count + price.cash_on_delivery
            # if self.payment_type == 'after_delivery':
            #     _sum += price.cost_of_delivery
            return _sum
        return 0

    def get_cost_of_delivery(self):
        price = self.get_price()
        if price:
            return price.cost_of_delivery
        return 0


class Order(models.Model):
    number = models.CharField(max_length=200, verbose_name=_('Unique number of order (it\'s a part of the url)'))
    magnets = models.ManyToManyField(Magnet, related_name='order', verbose_name=_('Magnets'), blank=True, null=True)
    status = models.CharField(choices=get_order_statuses(), max_length=200, verbose_name=_('Status'))

    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^(\+38)?0[0-9]{9}$')])
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)
    new_poshta_affiliate = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=200, choices=get_payment_types(), default=get_payment_types()[0][0])
    declaration_number = models.CharField(max_length=200, default='', null=True, blank=True)

    def set_empties(self):
        self.city = self.email = self.fio = self.new_poshta_affiliate = self.phone = 'empty'

    def create_order_num(self):
        self.number = get_random_string(10, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789') + md5(
            str(datetime.now())
        ).hexdigest()

    def get_count(self):
        return self.magnets.count()

    def get_price(self):
        count = self.get_count()
        price = Prices.objects.filter(Q(min_count__lte=count), Q(Q(max_count__gt=count) | Q(max_count=0)))
        if price:
            return price[0]
        return None

    def get_total_sum(self):
        count = self.get_count()
        price = self.get_price()
        if price:
            return price.magent_price * count
        return 0

    def get_total_sum_with_delivery(self):
        count = self.get_count()
        price = self.get_price()
        if price:
            _sum = price.magent_price * count + price.cash_on_delivery
            if self.payment_type == 'after_delivery':
                _sum += price.cost_of_delivery
            return _sum
        return 0

    def get_cost_of_delivery(self):
        price = self.get_price()
        if price:
            return price.cost_of_delivery
        return 0

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


from robokassa.signals import result_received


def payment_received(sender, **kwargs):
    order = Order.objects.get(pk=kwargs['InvId'])
    order.status = 'waiting_to_be_sent'
    order.save()

result_received.connect(payment_received)



class MagnetImage(models.Model):
    image = ImageField(verbose_name=_('Magnet image'), manual_crop=get_image_size())

    def __unicode__(self):
        return _('Magnet #%d') % self.pk

    class Meta:
        verbose_name = _('Image for magnet on main page')
        verbose_name_plural = _('Images for magnet on main page')


class Robokassa(models.Model):
    robokassa_login = models.CharField(max_length=100)
    robokassa_password1 = models.CharField(max_length=200)
    robokassa_password2 = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s : %s : %s" % (self.robokassa_login, self.robokassa_password1, self.robokassa_password2)

    class Meta:
        verbose_name = _('Robokassa payment system')
        verbose_name_plural = _('Robokassa payment systems')