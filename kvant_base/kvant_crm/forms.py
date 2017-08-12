# coding: utf-8
from models import Kvant, Customer, Transaction, SalaryReport
from django.forms import ModelForm

class AddOrderForm(ModelForm):

    class Meta:
        model = Kvant

        fields = ['status', 'customer', 'brand', 'model_item', 'serial_number', 'source',
                  'is_warranty', 'warranty_start', 'to_send', 'reason', 'look', 'additional',
                  'cost_repair', 'engineer', 'notes']


class AddCustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

class SalaryReportForm(ModelForm):

    class Meta:
        model = SalaryReport
        fields = ['item', 'engineer', 'part', 'repair_cost', 'paid_engineer']



class AddDebitForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['balance', 'debit', 'order_number', 'agent', 'notes']


class AddCreditForm(ModelForm):

   class Meta:
        model = Transaction
        fields = ['balance', 'credit', 'order_number', 'agent', 'notes']

class EditTransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['balance', 'debit', 'credit', 'order_number', 'agent', 'notes']


