# coding=utf-8
from django.contrib.admin.options import InlineModelAdmin

__author__ = 'djakson'
from django.contrib import admin
from models import MagnetImage, Order, Magnet, Prices, Robokassa


class MagnetImageAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'status', 'fio', 'phone', 'email', 'city', 'new_poshta_affiliate', 'payment_type']
    list_filter = ('status', 'payment_type')
    change_form_template = 'forms/admin/order.html'

admin.site.register(MagnetImage, MagnetImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Magnet)
admin.site.register(Prices)
admin.site.register(Robokassa)
