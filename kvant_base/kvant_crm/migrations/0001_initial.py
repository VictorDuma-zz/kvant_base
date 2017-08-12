# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='\u041a\u0432\u0430\u043d\u0442', max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430', blank=True)),
                ('current_balance', models.DecimalField(default=0, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441', max_digits=9, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0441\u0430',
                'verbose_name_plural': '\u041a\u0430\u0441\u0430',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=256, verbose_name='\u0406\u043c\u044f \u0442\u0430 \u043f\u0440\u0456\u0437\u0432\u0438\u0449\u0435')),
                ('phone', models.CharField(max_length=256, verbose_name='\u0442\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail', blank=True)),
                ('adress', models.CharField(max_length=256, verbose_name='\u0430\u0434\u0440\u0435\u0441\u0430', blank=True)),
                ('notes', models.CharField(max_length=256, verbose_name='\u041f\u0440\u0438\u043c\u0456\u0442\u043a\u0438', blank=True)),
            ],
            options={
                'ordering': ['contact_name'],
                'verbose_name': '\u041a\u043b\u0456\u0454\u043d\u0442',
                'verbose_name_plural': '\u041a\u043b\u0456\u0454\u043d\u0442\u0438',
            },
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=256, verbose_name='\u0406\u043c\u044f', blank=True)),
                ('surname', models.CharField(max_length=256, verbose_name='\u041f\u0440\u0456\u0437\u0432\u0438\u0449\u0435', blank=True)),
                ('name', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0406\u043d\u0436\u0435\u043d\u0435\u0440',
                'verbose_name_plural': '\u0406\u043d\u0436\u0435\u043d\u0435\u0440\u0438',
            },
        ),
        migrations.CreateModel(
            name='KindRepair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(default='nochoice', max_length=256, verbose_name='\u0442\u0435\u0445\u043d\u0456\u043a\u0430', choices=[('nochoice', '\u043d\u0435 \u0432\u0438\u0431\u0440\u0430\u043d\u043e'), ('warranty', '\u0413\u0430\u0440\u0430\u043d\u0442\u0456\u0439\u043d\u0438\u0439'), ('laptop', '\u041d\u043e\u0443\u0442\u0431\u0443\u043a'), ('monitor', '\u041c\u043e\u043d\u0456\u0442\u043e\u0440'), ('tab', '\u041f\u043b\u0430\u043d\u0448\u0435\u0442'), ('phone', '\u0421\u043c\u0430\u0440\u0442\u0444\u043e\u043d'), ('other', '\u0406\u043d\u0448\u0435')])),
                ('name', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430', blank=True)),
                ('paid_customer', models.DecimalField(default=0, verbose_name='\u0432\u0430\u0440\u0442\u0456\u0441\u0442\u044c \u0440\u043e\u0431\u043e\u0442\u0438', max_digits=9, decimal_places=2, blank=True)),
                ('paid_engineer', models.DecimalField(default=0, verbose_name='\u043e\u043f\u043b\u0430\u0442\u0430 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0443', max_digits=9, decimal_places=2, blank=True)),
            ],
            options={
                'verbose_name': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0438\u0442\u0438',
                'verbose_name_plural': '\u0412\u0438\u0434 \u0440\u043e\u0431\u0456\u0442',
            },
        ),
        migrations.CreateModel(
            name='Kvant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default='accept', max_length=256, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[('warnings', '\u0422\u0435\u0440\u043c\u0456\u043d\u043e\u0432\u043e'), ('accept', '\u041f\u0440\u0438\u0439\u043d\u044f\u0442\u043e'), ('active', '\u041f\u043e\u0433\u043e\u0434\u0436\u0435\u043d\u043d\u044f'), ('wait', '\u041e\u0447\u0456\u043a\u0443\u0432\u0430\u043d\u043d\u044f \u0437\u0430\u043f\u0447\u0430\u0441\u0442\u0438\u043d'), ('info', '\u0412 \u0440\u043e\u0431\u043e\u0442\u0456'), ('done', '\u0412\u0438\u043a\u043e\u043d\u0430\u043d\u043e'), ('success', '\u041a\u043b\u0456\u0454\u043d\u0442 \u0456\u043d\u0444\u043e\u0440\u043c\u043e\u0432\u0430\u043d\u0438\u0439'), ('closed', '\u0417\u0430\u043a\u0440\u0438\u0442\u043e')])),
                ('date_now', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('date_close', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u0438\u0442\u0442\u044f', blank=True)),
                ('is_warranty', models.BooleanField(default=False, verbose_name='\u0413\u0430\u0440\u0430\u043d\u0442\u0456\u044f', choices=[(True, '\u0433\u0430\u0440\u0430\u043d\u0442\u0456\u044f'), (False, '\u043d\u0435 \u0433\u0430\u0440\u0430\u043d\u0442\u0456\u044f')])),
                ('to_send', models.CharField(default='Not', choices=[('Not', '\u041d\u0456'), ('PHOTORVICE', '\u0424\u043e\u0442\u043e\u0441\u0435\u0440\u0432\u0456\u0441 '), ('PHOTORVICE_REPORT', '\u0424\u043e\u0442\u043e\u0441\u0435\u0440\u0432\u0456\u0441 \u0437\u0432\u0456\u0442'), ('KROK', '\u041a\u0440\u043e\u043a'), ('ASSISTANT', '\u0410\u0441\u0456\u0441\u0442\u0435\u043d\u0442')], max_length=256, blank=True, null=True, verbose_name='\u0412\u0456\u0434\u043f\u0440\u0430\u0432\u043a\u0430')),
                ('brand', models.CharField(max_length=256, null=True, verbose_name='\u0411\u0440\u0435\u043d\u0434')),
                ('model_item', models.CharField(max_length=256, null=True, verbose_name='\u041c\u043e\u0434\u0435\u043b\u044c', blank=True)),
                ('serial_number', models.CharField(max_length=256, null=True, verbose_name='\u0421\u0435\u0440\u0456\u0439\u043d\u0438\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True)),
                ('reason', models.CharField(max_length=256, null=True, verbose_name='\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u0430 \u043d\u0435\u0441\u043f\u0440\u0430\u0432\u043d\u0456\u0441\u0442\u044c', blank=True)),
                ('look', models.CharField(max_length=256, null=True, verbose_name='\u0417\u043e\u0432\u043d\u0456\u0448\u043d\u0456\u0439 \u0432\u0438\u0433\u043b\u044f\u0434', blank=True)),
                ('warranty_start', models.DateField(null=True, verbose_name='\u041f\u043e\u0447\u0430\u0442\u043e\u043a \u0433\u0430\u0440\u0430\u043d\u0442\u0456', blank=True)),
                ('additional', models.CharField(max_length=256, null=True, verbose_name='\u041a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0430\u0446\u0456\u044f', blank=True)),
                ('source', models.CharField(max_length=256, null=True, verbose_name='\u0420\u0435\u043a\u043b\u0430\u043c\u0430', choices=[('Not', '\u041d\u0456'), ('NET', '\u0406\u043d\u0442\u0435\u0440\u043d\u0435\u0442'), ('FACEBOOK', '\u0424\u0435\u0439\u0441\u0431\u0443\u043a'), ('TRANSPORT', '\u041c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0430'), ('ADVISE', '\u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0430\u0446\u0456\u044f'), ('SHOP', '\u041c\u0430\u0433\u0430\u0437\u0438\u043d')])),
                ('cost_repair', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, null=True, verbose_name='\u0412\u0430\u0440\u0442\u0456\u0441\u0442\u044c \u0440\u0435\u043c\u043e\u043d\u0442\u0443')),
                ('pay_engineer', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, null=True, verbose_name='\u041e\u043f\u043b\u0430\u0442\u0430 \u0456\u043d\u0436\u0435\u043d\u0435\u0440\u0443')),
                ('is_paid', models.BooleanField(default=False, verbose_name='\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u043e', choices=[(True, '\u0422\u0430\u043a'), (False, '\u041d\u0456')])),
                ('paid_date', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u043b\u0430\u0442\u0438', blank=True)),
                ('notes', models.CharField(max_length=256, verbose_name='\u041f\u0440\u0438\u043c\u0456\u0442\u043a\u0438', blank=True)),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='\u0424\u043e\u0442\u043e', blank=True)),
                ('customer', models.ForeignKey(verbose_name='\u041a\u043b\u0456\u0454\u043d\u0442', blank=True, to='kvant_crm.Customer', null=True)),
                ('engineer', models.ManyToManyField(to='kvant_crm.Engineer', verbose_name='\u0406\u043d\u0436\u0435\u043d\u0435\u0440', blank=True)),
                ('kind_repair', models.ManyToManyField(to='kvant_crm.KindRepair', verbose_name='\u0412\u0438\u0434 \u0440\u043e\u0431\u043e\u0442\u0438', blank=True)),
            ],
            options={
                'ordering': ['-date_now'],
                'verbose_name': '\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f',
                'verbose_name_plural': '\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debit', models.DecimalField(default=0, verbose_name='\u041d\u0430\u0434\u0445\u043e\u0434\u0436\u0435\u043d\u043d\u044f', max_digits=9, decimal_places=2, blank=True)),
                ('credit', models.DecimalField(default=0, verbose_name='\u0412\u0438\u0442\u0440\u0430\u0442\u0438', max_digits=9, decimal_places=2, blank=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('notes', models.CharField(max_length=256, verbose_name='\u041d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('agent', models.ForeignKey(verbose_name='\u041a\u043e\u043d\u0442\u0440\u0430\u0433\u0435\u043d\u0442', blank=True, to='kvant_crm.Customer', null=True)),
                ('balance', models.ForeignKey(default='\u041a\u0432\u0430\u043d\u0442', to='kvant_crm.Balance')),
                ('order_number', models.ForeignKey(verbose_name='\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f', blank=True, to='kvant_crm.Kvant', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u0422\u0440\u0430\u043d\u0437\u0430\u0446\u0456\u044f',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0437\u0430\u0446\u0456\u0457',
            },
        ),
    ]
