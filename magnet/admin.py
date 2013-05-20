# coding=utf-8
from django.contrib.admin.options import InlineModelAdmin

__author__ = 'djakson'
from django.contrib import admin
from models import MagnetImage, Order, Magnet

class MagnetImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(MagnetImage, MagnetImageAdmin)
admin.site.register(Order)
admin.site.register(Magnet)
