# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kvant_crm', '0004_auto_20170407_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part', models.CharField(max_length=256, verbose_name='\u0417\u0430\u043f\u0447\u0430\u0441\u0442\u0438\u043d\u0430', blank=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u043e', choices=[(False, '\u041d\u0456'), (True, '\u0422\u0430\u043a')])),
                ('repair_cost', models.DecimalField(default=0, verbose_name='\u0432\u0430\u0440\u0442\u0456\u0441\u0442\u044c \u0440\u043e\u0431\u043e\u0442\u0438', max_digits=9, decimal_places=2, blank=True)),
                ('paid_engineer', models.DecimalField(default=0, verbose_name='\u043e\u043f\u043b\u0430\u0442\u0430 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0443', max_digits=9, decimal_places=2, blank=True)),
                ('paid_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u0438', blank=True)),
                ('engineer', models.ForeignKey(verbose_name='\u0406\u043d\u0436\u0435\u043d\u0435\u0440', to='kvant_crm.Engineer')),
            ],
            options={
                'verbose_name': '\u0417\u0432\u0456\u0442 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0430',
                'verbose_name_plural': '\u0417\u0432\u0456\u0442\u0438 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0430',
            },
        ),
        migrations.AlterModelOptions(
            name='kindrepair',
            options={'ordering': ['item'], 'verbose_name': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0438\u0442\u0438', 'verbose_name_plural': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0456\u0442'},
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='kind_repair',
        ),
        migrations.RemoveField(
            model_name='kvant',
            name='paid_date',
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
        migrations.AddField(
            model_name='salaryreport',
            name='item',
            field=models.ForeignKey(verbose_name='\u0432\u0438\u0434 \u0440\u043e\u0431\u043e\u0442\u0438', to='kvant_crm.KindRepair'),
        ),
        migrations.AddField(
            model_name='salaryreport',
            name='repair',
            field=models.ForeignKey(verbose_name='\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f', to='kvant_crm.Kvant'),
        ),
    ]
