# coding=utf-8
# Create your views here.
import os
import tempfile
import zipfile
from django.core.servers.basehttp import FileWrapper
from zipfile import ZipFile
from hashlib import sha1
import urllib2
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader, Context, RequestContext
from django.utils import simplejson
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from models import Magnet, Order, get_order
from imagnet.settings import cur
from magnet.cms_plugins import MagnetForm
from robokassa.forms import RobokassaForm
from django.contrib import messages


class OrderForm(ModelForm):
    class Meta:
        model = Order


def save(request):
    if request.POST and request.is_ajax():
        magnet = Magnet()
        magnet.image = request.POST.get('previewUrl', '')
        magnet.save()
        order = get_order(request, draft=True)
        order.save()
        order.magnets.add(magnet)
        data = serializers.serialize("json", [order])
        return HttpResponse(content=data, content_type='application/json')
    return HttpResponse('access denied!')


def validate(request):
    if request.is_ajax():
        data = request.POST
        if data:
            form = OrderForm(data=data)
            if form.is_valid():
                return HttpResponse(content=simplejson.dumps({'valid': True, 'errors': []}),
                                    mimetype="application/json")
            else:
                return HttpResponse(content=simplejson.dumps({'valid': False, 'errors': form.errors.keys()}),
                                    mimetype="application/json")
        else:
            raise Http404
    else:
        raise Http404


def order(request, order_num=None):
    """

    """
    custom_context = {'editable': False, 'uc_form': MagnetForm()}
    if order_num is not None:
        custom_context.update({'order_num': order_num})
        order_obj = get_object_or_404(Order, number=order_num)
        if order_obj.status == 'new':
            raise Http404
        custom_context['pay_form'] = RobokassaForm(initial={
               'OutSum': order_obj.get_total_sum_with_delivery(),
               'InvId': order_obj.pk,
               'Desc': order_obj.fio,
               'Email': order_obj.email,
               #'IncCurrLabel': 'UAH',
               'Culture': 'ru'
           })
    else:
        custom_context['editable'] = True
        order_obj = get_order(request, draft=True)
    form = OrderForm(instance=order_obj)
    custom_context.update({'order': order_obj})
    custom_context.update({'form': form})
    return render(request, 'order.html', custom_context)


def create_order(request):
    if request.POST:
        post = request.POST.copy()
        order_num = request.session.get('order_num', None)
        if order_num:  # если есть номер заказа в сессии
            order_obj = get_order(request, draft=True)  # получаем черновой заказ
            post.update({
                'number': order_obj.number,
                'status': 'waiting_for_payment' if post.get('payment_type') == 'online' else 'waiting_to_be_sent'
            })
            order_form = OrderForm(data=post)
            print  order_form.initial
            if order_form.is_valid():
                _order_new = order_form.save()
                for magnet in order_obj.magnets.all():
                    _order_new.magnets.add(magnet)
                order_obj.delete()
                request.session['order_num'] = None
            else:
                return HttpResponse(content=simplejson.dumps(list(order_form.errors.viewitems())),
                                    mimetype='application/json')
            resp = {'redirect_to': reverse('get_order', kwargs={'order_num': order_num})}
            return HttpResponse(simplejson.dumps(resp), mimetype='application/json')
        else:
            return redirect(reverse('main_page'))
    else:
        raise Http404


def duplicate(request):
    if request.is_ajax() and request.POST:
        magnet_id = request.POST.get('donor_id', None)
        if magnet_id:
            magnet = get_object_or_404(Magnet, pk=magnet_id)
            new_magnet = Magnet()
            new_magnet.image = magnet.image
            new_magnet.save()
            try:
                new_magnet.order_draft.add(magnet.order_draft.get())
            except ObjectDoesNotExist, ex:
                new_magnet.delete()
            return HttpResponse(simplejson.dumps({"id": new_magnet.pk, "image": new_magnet.image.cdn_url}), mimetype="application/json")
        else:
            raise Http404
    raise Http404

def delete(request):
    if request.is_ajax() and request.POST:
        magnet_id = request.POST.get('target_id', None)
        if magnet_id:
            magnet = get_object_or_404(Magnet, pk=magnet_id)
            magnet.delete()
            return HttpResponse(simplejson.dumps({}), mimetype="application/json")
        else:
            raise Http404
    raise Http404


def edit(request):
    if request.is_ajax() and request.POST:
        magnet_id = request.POST.get('target_id', None)
        if magnet_id:
            magnet = get_object_or_404(Magnet, pk=magnet_id)
            image = request.POST.get('cdnUrl', None)
            if image:
                magnet.image = image
                magnet.save()
            else:
                raise Http404
            return HttpResponse(simplejson.dumps({'image': image}), mimetype="application/json")
        else:
            raise Http404
    raise Http404


def __download(url, dir, append=''):
    file_name = sha1(url).hexdigest() + append
    u = urllib2.urlopen(url)
    f = open(os.path.join(dir, file_name), 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 20480
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8) * (len(status) + 1)
        #print status,
    f.close()
    return os.path.join(dir, file_name), file_name


def export(request):
    if request.POST:
        tmp_dir = cur('tmp')
        order_id = request.POST.get('target_id', None)
        if order_id:
            order_obj = get_object_or_404(Order, pk=order_id)
            temp = tempfile.TemporaryFile()
            with ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as order_zip:
                for magnet in order_obj.magnets.all():
                    filename, archname = __download(magnet.image.__str__(), tmp_dir, append='.jpg')
                    order_zip.write(filename, archname)
                description_filename = os.path.join(tmp_dir, u"%s Заказ №%d" % (order_obj.fio, order_obj.pk))
                info_template = loader.get_template('order_info.txt')
                info_context = RequestContext(request).update(Context({'order': order_obj}))
                tmp = open(description_filename, 'w')
                tmp.write(info_template.render(info_context).encode('utf8'))
                tmp.close()
                order_zip.write(description_filename, u"%s Заказ №%d.txt" % (order_obj.fio, order_obj.pk))
                del description_filename
            wrapper = FileWrapper(temp)
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s' % ('order_%s.zip' % order_obj.pk)
            response['Content-Length'] = temp.tell()
            temp.seek(0)
            return response
        else:
            raise Http404
    raise Http404


from django.views.decorators.csrf import csrf_exempt
from robokassa.conf import USE_POST
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa.models import SuccessNotification
from robokassa.signals import result_received, success_page_visited, fail_page_visited


@csrf_exempt
def payment_result(request):
    data = request.POST if USE_POST else request.GET
    form = ResultURLForm(data)
    print data.get('SignatureValue')
    if form.is_valid():
        order_id, order_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # сохраняем данные об успешном уведомлении в базе, чтобы
        # можно было выполнить дополнительную проверку на странице успешного
        # заказа
        notification = SuccessNotification.objects.create(InvId=order_id, OutSum=order_sum)

        # дополнительные действия с заказом (например, смену его статуса) можно
        # осуществить в обработчике сигнала robokassa.signals.result_received
        result_received.send(sender=notification, InvId=order_id, OutSum=order_sum,
                             extra=form.extra_params())

        return HttpResponse('OK%s' % order_id)
    return HttpResponse('error: bad signature')


@csrf_exempt
def payment_fail(request):
    data = request.POST if USE_POST else request.GET
    form = FailRedirectForm(data)
    messages.error(request, 'При оплате произошла ошибка')
    if form.is_valid():
        order_id, order_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # дополнительные действия с заказом (например, смену его статуса для
        # разблокировки товара на складе) можно осуществить в обработчике
        # сигнала robokassa.signals.fail_page_visited
        fail_page_visited.send(sender = form, InvId = order_id, OutSum = order_sum,
                               extra = form.extra_params())

        order_obj = get_object_or_404(Order, pk=order_id)
        return redirect(to=reverse('get_order', kwargs={'order_num': order_obj.number}))
    order_obj = get_order(request, False)
    return redirect(to=reverse('get_order', kwargs={'order_num': order_obj.number}))



@csrf_exempt
def payment_success(request):
    data = request.POST if USE_POST else request.GET
    form = SuccessRedirectForm(data)
    #context = {'InvId': data.get('InvId'), 'OutSum': data.get('OutSum'), 'form': form}
    #return render(request, template_name, context)
    if form.is_valid():
        order_id, order_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # в случае, когда не используется строгая проверка, действия с заказом
        # можно осуществлять в обработчике сигнала robokassa.signals.success_page_visited
        success_page_visited.send(sender = form, InvId = order_id, OutSum = order_sum,
                                  extra = form.extra_params())

        messages.success(request, 'Оплата прошла успешно')
        # context = {'InvId': order_id, 'OutSum': order_sum, 'form': form}
        # context.update(form.extra_params())
        # context.update(extra_context or {})
        #return render(request, template_name, context)
        order_obj = get_object_or_404(Order, pk=order_id)
        return redirect(to=reverse('get_order', kwargs={'order_num': order_obj.number}))

    messages.error(request, 'При оплате произошла ошибка')
    order_obj = get_order(request)
    return redirect(to=reverse('get_order', kwargs={'order_num': order_obj.number}))


def payment_received(sender, **kwargs):
    order = Order.objects.get(pk=kwargs['InvId'])
    order.status = 'waiting_to_be_sent'
    order.save()


def payment_fail(sender, **kwargs):
    order = Order.objects.get(pk=kwargs['InvId'])
    order.status = 'waiting_for_payment'
    order.save()


fail_page_visited.connect(payment_fail)

result_received.connect(payment_received)