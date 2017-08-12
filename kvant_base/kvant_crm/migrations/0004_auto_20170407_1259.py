# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kvant_crm', '0003_auto_20170407_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='kvant',
            name='kind_repair',
            field=models.ManyToManyField(to='kvant_crm.KindRepair', verbose_name='\u0412\u0438\u0434 \u0440\u043e\u0431\u043e\u0442\u0438', blank=True),
        ),
        migrations.AddField(
            model_name='kvant',
            name='pay_engineer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, null=True, verbose_name='\u041e\u043f\u043b\u0430\u0442\u0430 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0443'),
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='engineer',
        ),
        migrations.AddField(
            model_name='kvant',
            name='engineer',
            field=models.ManyToManyField(to='kvant_crm.Engineer', verbose_name='\u0406\u043d\u0436\u0435\u043d\u0435\u0440', blank=True),
        ),
    ]
