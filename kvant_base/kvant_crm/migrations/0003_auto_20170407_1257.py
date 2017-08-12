# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kvant_crm', '0002_auto_20170406_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryreport',
            name='engineer',
        ),
        migrations.RemoveField(
            model_name='salaryreport',
            name='item',
        ),
        migrations.RemoveField(
            model_name='salaryreport',
            name='repair',
        ),
        migrations.AlterModelOptions(
            name='kindrepair',
            options={'verbose_name': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0438\u0442\u0438', 'verbose_name_plural': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0456\u0442'},
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='kind_repair',
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='pay_engineer',
        ),
        migrations.AddField(
            model_name='kvant',
            name='paid_date',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u0438', blank=True),
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='engineer',
        ),
        migrations.AddField(
            model_name='kvant',
            name='engineer',
            field=models.ForeignKey(verbose_name='\u0406\u043d\u0436\u0435\u043d\u0435\u0440', blank=True, to='kvant_crm.Engineer', null=True),
        ),
        migrations.DeleteModel(
            name='SalaryReport',
        ),
    ]
