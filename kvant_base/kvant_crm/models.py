# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User

from datetime import datetime
from decimal import Decimal

from django.db import models



STATUS = [
    ('warnings', 'Терміново'),
    ('accept', 'Прийнято'),
    ('active', 'Погодження'),
    ('decision', 'Рішення клієнта'),
    ('wait', 'Очікування запчастин'),
    ('info', 'В роботі'),
    ('done', 'Виконано'),
    ('success', 'Клієнт інформований'),
    ('closed', 'Закрито'),
]

REPAIRS = [
    ('nochoice', 'не вибрано'),
    ('warranty', 'Гарантійний'),
    ('laptop', 'Ноутбук'),
    ('monitor', 'Монітор'),
    ('tab', 'Планшет'),
    ('phone', 'Смартфон'),
    ('other', 'Інше'),
]

SENDING = [
    ('Not', 'Ні'),
    ('PHOTORVICE', 'Фотосервіс '),
    ('PHOTORVICE_REPORT', 'Фотосервіс звіт'),
    ('KROK', 'Крок'),
    ('ASSISTANT', 'Асістент'),
    ]

SOURCE = [
    ('Not', 'Ні'),
    ('NET', 'Інтернет'),
    ('FACEBOOK', 'Фейсбук'),
    ('TRANSPORT', 'Маршрутка'),
    ('ADVISE', 'Рекомендація'),
    ('SHOP', 'Магазин'),
    ]

class Kvant(models.Model):
    class Meta(object):
        ordering = ['-date_now']
        verbose_name = u"Замовлення"
        verbose_name_plural = u"Замовлення"


    status = models.CharField(
        max_length=256,
        choices=STATUS,
        default='accept',
        verbose_name=u"Статус")

    customer = models.ForeignKey('Customer',

                                 blank=True,
                                 null=True,
                                 verbose_name=u"Клієнт")

    date_now = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        blank=False,
        verbose_name=u"Дата")

    date_close = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name=u"Дата закриття")


    is_warranty = models.BooleanField(
        default= False,
        choices=((True, 'гарантія'), (False, 'не гарантія')),
        verbose_name=u"Гарантія"
    )

    to_send = models.CharField(
        max_length=256,
        default='Not',
        blank=True,
        null=True,
        choices=SENDING,
        verbose_name=u"Відправка"
    )

    brand = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        verbose_name=u"Бренд")

    model_item = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Модель")

    serial_number = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Серійний номер")

    reason = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Заявлена несправність")

    look = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Зовнішній вигляд")

    warranty_start = models.DateField(
        auto_now=False,
        blank=True,
        null = True,
        verbose_name=u"Початок гаранті")


    additional = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Комплектація")


    source = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        choices=SOURCE,
        verbose_name=u"Реклама"
    )

    engineer = models.ForeignKey('Engineer',blank=True, null=True, verbose_name=u"Інженер")

    cost_repair = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name=u"Вартість ремонту")

    pay_engineer = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        verbose_name=u"Оплата інженеру")


    is_paid = models.BooleanField(default=False,
                                  choices=((True, 'Так'), (False, 'Ні')),
                                  verbose_name=u"Оплачено")


    notes = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Примітки")

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    def __unicode__(self):
        return u"%s %s" % (self.pk, self.customer)

    def close_order(self):
        self.date_close = datetime.now()
        self.status = 'closed'

    def send_order(self):
        self.status = 'wait'



class Customer(models.Model):
    class Meta(object):
        ordering = ['contact_name']
        verbose_name = u"Клієнт"
        verbose_name_plural = u"Клієнти"

    contact_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Імя та прізвище")

    phone = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"телефон")

    email = models.EmailField(
        blank=True,
        verbose_name=u"E-mail")

    adress = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"адреса")

    notes = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Примітки")

    def __unicode__(self):
        return u"%s %s" % (self.contact_name, self.phone)


class Engineer(models.Model):
    class Meta(object):
        verbose_name = u"Інженер"
        verbose_name_plural = u"Інженери"

    name = models.ForeignKey(User)

    nickname = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Імя")

    surname = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Прізвище")

    def __unicode__(self):
        return u"%s %s" % (self.nickname, self.surname)


class Balance(models.Model):

    class Meta(object):
        verbose_name = u"Каса"
        verbose_name_plural = u"Каса"

    name = models.CharField(
        default='Квант',
        max_length=256,
        blank=True,
        verbose_name=u"Назва")

    current_balance = models.DecimalField(verbose_name=u"Баланс", max_digits=9, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.current_balance)

    def balance_credit(self, credit):

        if credit < 0:
            raise ValueError('Invalid amount')

        self.credit=-credit,
        self.current_balance -= credit
        self.save()

    def balance_debit(self, debit):

        if debit < 0:
            raise ValueError('Invalid amount')

        self.current_balance += debit
        self.save()

class Transaction(models.Model):

    class Meta(object):
        verbose_name = u"Транзація"
        verbose_name_plural = u"Транзації"
        ordering = ['-pk']

    balance = models.ForeignKey(Balance, default='Квант')
    debit = models.DecimalField(verbose_name=u"Надходження", max_digits=9, decimal_places=2, default=0, blank=True)
    credit = models.DecimalField(verbose_name=u"Витрати", max_digits=9, decimal_places=2, default=0, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    order_number = models.ForeignKey(Kvant, verbose_name=u"Замовлення", blank=True, null=True)
    agent = models.ForeignKey(Customer, verbose_name=u"Контрагент", blank=True, null=True)
    notes = models.CharField(verbose_name=u"Нотатки", max_length=256, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.id, self.created_at)


class KindRepair(models.Model):

    class Meta(object):
        verbose_name = u"Вид робити"
        verbose_name_plural = u"Вид робіт"
        ordering = ['item']

    item = models.CharField(
        max_length=256,
        choices=REPAIRS,
        default='nochoice',
        verbose_name=u"техніка")
    name = models.CharField(verbose_name=u"Назва", max_length=256, blank=True)
    paid_customer = models.DecimalField(verbose_name=u"вартість роботи", max_digits=9, decimal_places=2, default=0, blank=True)
    paid_engineer = models.DecimalField(verbose_name=u"оплата інженеру", max_digits=9, decimal_places=2, default=0, blank=True)



    def __unicode__(self):
        return u"%s %s %s" % (self.get_item_display(), self.name, self.paid_customer)

class SalaryReport(models.Model):

    class Meta(object):
        verbose_name = u"Звіт інженера"
        verbose_name_plural = u"Звіти інженера"

    item = models.ForeignKey(KindRepair, verbose_name=u"вид роботи", blank=False)
    engineer = models.ForeignKey(Engineer, blank=False, verbose_name=u"Інженер")
    repair = models.ForeignKey(Kvant, blank=False, verbose_name=u"Замовлення")
    part = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Запчастина")
    is_paid = models.BooleanField(default=False,
                                  choices=((False, 'Ні'), (True, 'Так')),
                                  verbose_name=u"Оплачено")
    repair_cost = models.DecimalField(verbose_name=u"вартість роботи", max_digits=9, decimal_places=2, default=0, blank=True)
    paid_engineer = models.DecimalField(verbose_name=u"оплата інженеру", max_digits=9, decimal_places=2, default=0,
                                        blank=True)
    paid_date = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name=u"Дата оплати")


    def __unicode__(self):
        return u"%s %s" % (self.repair, self.item)

