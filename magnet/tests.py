"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

from models import *
from views import OrderForm


class OrderDraftTest(TestCase):

    def test_create_order(self):
        order_draft = OrderDraft()
        order_draft.create_order_num()

        for i in xrange(0,5):
            magnet = Magnet()
            magnet.image = 'test %d' % i
            magnet.save()
            order_draft.magnets.add(magnet)

        form = OrderForm(data={'fio': 'Djakson White'})

        if form.is_valid():
            self.assertTrue(True, True)
        else:
            print form.errors