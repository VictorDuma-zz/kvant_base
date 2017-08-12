# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.db import models
from django.core.urlresolvers import reverse



class Repair(models.Model):

    repair_title = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        verbose_name=u"Заголовок")

    repair_photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    repair_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Текст")

    def __unicode__(self):
        return u"%s %s" % (self.repair_title, self.repair_title)


class Warranty(models.Model):

    warranty_title = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        verbose_name=u"Заголовок")

    warranty_photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    warranty_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Текст")

    def __unicode__(self):
        return u"%s %s" % (self.id, self.warranty_title)

class Certificate(models.Model):

    certificate_title = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        verbose_name=u"Заголовок")

    certificate_photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    def __unicode__(self):
        return u"%s %s" % (self.id, self.certificate_title)

