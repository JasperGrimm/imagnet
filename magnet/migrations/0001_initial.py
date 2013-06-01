# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MagnetPlugin'
        db.create_table('cmsplugin_magnetplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('image', self.gf('pyuploadcare.dj.models.ImageField')(null=True, blank=True)),
        ))
        db.send_create_signal('magnet', ['MagnetPlugin'])

        # Adding model 'Magnet'
        db.create_table('magnet_magnet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('pyuploadcare.dj.models.ImageField')(null=True, blank=True)),
        ))
        db.send_create_signal('magnet', ['Magnet'])

        # Adding model 'Prices'
        db.create_table('magnet_prices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('min_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1000)),
            ('max_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1000)),
            ('magent_price', self.gf('django.db.models.fields.DecimalField')(max_length=10000, max_digits=100000, decimal_places=2)),
            ('cash_on_delivery', self.gf('django.db.models.fields.DecimalField')(max_length=10000, max_digits=100000, decimal_places=2)),
            ('cost_of_delivery', self.gf('django.db.models.fields.DecimalField')(max_length=10000, max_digits=100000, decimal_places=2)),
        ))
        db.send_create_signal('magnet', ['Prices'])

        # Adding model 'OrderDraft'
        db.create_table('magnet_orderdraft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('magnet', ['OrderDraft'])

        # Adding M2M table for field magnets on 'OrderDraft'
        db.create_table('magnet_orderdraft_magnets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('orderdraft', models.ForeignKey(orm['magnet.orderdraft'], null=False)),
            ('magnet', models.ForeignKey(orm['magnet.magnet'], null=False))
        ))
        db.create_unique('magnet_orderdraft_magnets', ['orderdraft_id', 'magnet_id'])

        # Adding model 'Order'
        db.create_table('magnet_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('new_poshta_affiliate', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='online', max_length=200)),
        ))
        db.send_create_signal('magnet', ['Order'])

        # Adding M2M table for field magnets on 'Order'
        db.create_table('magnet_order_magnets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['magnet.order'], null=False)),
            ('magnet', models.ForeignKey(orm['magnet.magnet'], null=False))
        ))
        db.create_unique('magnet_order_magnets', ['order_id', 'magnet_id'])

        # Adding model 'MagnetImage'
        db.create_table('magnet_magnetimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('pyuploadcare.dj.models.ImageField')()),
        ))
        db.send_create_signal('magnet', ['MagnetImage'])

        # Adding model 'Robokassa'
        db.create_table('magnet_robokassa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('robokassa_login', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('robokassa_password1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('robokassa_password2', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('magnet', ['Robokassa'])


    def backwards(self, orm):
        # Deleting model 'MagnetPlugin'
        db.delete_table('cmsplugin_magnetplugin')

        # Deleting model 'Magnet'
        db.delete_table('magnet_magnet')

        # Deleting model 'Prices'
        db.delete_table('magnet_prices')

        # Deleting model 'OrderDraft'
        db.delete_table('magnet_orderdraft')

        # Removing M2M table for field magnets on 'OrderDraft'
        db.delete_table('magnet_orderdraft_magnets')

        # Deleting model 'Order'
        db.delete_table('magnet_order')

        # Removing M2M table for field magnets on 'Order'
        db.delete_table('magnet_order_magnets')

        # Deleting model 'MagnetImage'
        db.delete_table('magnet_magnetimage')

        # Deleting model 'Robokassa'
        db.delete_table('magnet_robokassa')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'magnet.magnet': {
            'Meta': {'object_name': 'Magnet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('pyuploadcare.dj.models.ImageField', [], {'null': 'True', 'blank': 'True'})
        },
        'magnet.magnetimage': {
            'Meta': {'object_name': 'MagnetImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('pyuploadcare.dj.models.ImageField', [], {})
        },
        'magnet.magnetplugin': {
            'Meta': {'object_name': 'MagnetPlugin', 'db_table': "'cmsplugin_magnetplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('pyuploadcare.dj.models.ImageField', [], {'null': 'True', 'blank': 'True'})
        },
        'magnet.order': {
            'Meta': {'object_name': 'Order'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magnets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'order'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['magnet.Magnet']"}),
            'new_poshta_affiliate': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'online'", 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'magnet.orderdraft': {
            'Meta': {'object_name': 'OrderDraft'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magnets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'order_draft'", 'symmetrical': 'False', 'to': "orm['magnet.Magnet']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'magnet.prices': {
            'Meta': {'object_name': 'Prices'},
            'cash_on_delivery': ('django.db.models.fields.DecimalField', [], {'max_length': '10000', 'max_digits': '100000', 'decimal_places': '2'}),
            'cost_of_delivery': ('django.db.models.fields.DecimalField', [], {'max_length': '10000', 'max_digits': '100000', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magent_price': ('django.db.models.fields.DecimalField', [], {'max_length': '10000', 'max_digits': '100000', 'decimal_places': '2'}),
            'max_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1000'}),
            'min_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1000'})
        },
        'magnet.robokassa': {
            'Meta': {'object_name': 'Robokassa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'robokassa_login': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'robokassa_password1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'robokassa_password2': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['magnet']