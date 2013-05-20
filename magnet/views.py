# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from models import Magnet, Order, get_order, new_order
from django.core import serializers
from cms.api import Page
from django.shortcuts import get_object_or_404


def save(request):
    if request.POST and request.is_ajax():
        from django.utils.simplejson import dumps
        magnet = Magnet()
        magnet.image = request.POST.get('previewUrl', '')
        magnet.save()
        order = get_order(request)
        if order.status != 'new': # if order is not NEW, we can't change it
            order = new_order(request)
        order.save()
        order.magnets.add(magnet)
        data = serializers.serialize("json", [order,])
        return HttpResponse(content=data,content_type='application/json')
    return HttpResponse('access denied!')

def order(request, order_num=None):
    custom_context = {}
    if order_num is not None:
        custom_context.update({'order_num':order_num})
        order_obj = get_object_or_404(Order, number=order_num)
        if order_obj.status == 'new':
            raise Http404
    else:
        order_obj = get_order(request)
    custom_context.update({'order': order_obj})
    from cms.utils import page_resolver
    request.path = '/order'
    page = page_resolver.get_page_from_request(request)
    return render(request, 'order.html', custom_context)

def create_order(request):
    if request.POST:
        post = request.POST
        order_num = request.session.get('order_num', None)
        if order_num:
            order = get_order(request)
            if post.get('payment_type', None) == 'online':
                order.status = 'waiting_for_payment'
            else:
                order.status = 'waiting_to_be_sent'
            order.fio = post.get('fio', None)
            order.city = post.get('city', None)
            order.email = post.get('email', None)
            order.phone = post.get('phone', None)
            order.new_poshta_affiliate = post.get('new_poshta_affiliate', 0)
            try:
                order.save()
            except Exception, e:
                print e.args
            return redirect(reverse('get_order', kwargs={'order_num': order_num}))
        else:
            return redirect(reverse('main_page'))
    else:
        raise Http404