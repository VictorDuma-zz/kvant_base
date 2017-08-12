# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from models import Kvant, Customer, Transaction, Balance, Engineer, SalaryReport
from forms import AddOrderForm, AddCustomerForm, AddDebitForm, AddCreditForm, SalaryReportForm
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import render_to_response
from django.db.models import F, Q, Sum, FloatField
from datetime import datetime
import xlrd
from xlutils.copy import copy
import xlwt
import os
import json



class ListCustomers(TemplateView):
    template_name = 'customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListCustomers, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.all()
        return context



class ListPaid(TemplateView):
    template_name = 'paid_list.html'

    def get_context_data(self, **kwargs):

        context = super(ListPaid, self).get_context_data(**kwargs)
        context['repairs'] = SalaryReport.objects.filter(is_paid=True)
        return context



class PaidEngineer(TemplateView):
    template_name = 'paid.html'

    def get_context_data(self, **kwargs):
        context = super(PaidEngineer, self).get_context_data(**kwargs)

        queryset_paid = SalaryReport.objects.filter(is_paid=False, engineer__pk__in=self.kwargs['pk'])
        context['balance'] = Balance.objects.get(name='Квант')
        context['repairs'] = queryset_paid
        context['repairs_id'] = self.kwargs['pk']


        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        paid_engineer = data['paid_engineer']

        try:
            paid_engineer = Decimal(paid_engineer)
        except:
            ValueError

        is_paid = data['is_paid'] and True or False
        repair = SalaryReport.objects.get(pk=data['pk'])

        setattr(repair, 'is_paid', is_paid)
        repair.paid_date = datetime.now()
        repair.save()


        return JsonResponse({'status': 'success'})


@login_required
def kvant_base(request):
    engineers = Engineer.objects.all()
    balance = Balance.objects.get(name='Квант')
    customers = Customer.objects.all()
    tables = Kvant.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'customer', 'brand', 'status', 'engineer'):
        tables = tables.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            tables = tables.reverse()
    return render(request, 'kvant.html', {'tables': tables, 'balance': balance, 'engineers': engineers, 'customers': customers})


@login_required
def finance(request):
    engineers = Engineer.objects.all()
    customers = Customer.objects.all()
    transactions = Transaction.objects.all()
    debit_sum = Transaction.objects.all().aggregate(Sum('debit', output_field=FloatField()))
    balance = Balance.objects.get(name='Квант')
    return render(request, 'finance.html', {'transactions': transactions, 'debit_sum': debit_sum,
                                            'balance': balance, 'engineers': engineers, 'customers': customers})


# TO DO
# def create_pdf(*args, **kwargs):
#     return

@login_required
def order_doc(request, pk):
    order = get_object_or_404(Kvant, pk=pk)
    return render(request, 'order_doc.html', {'order': order})

@login_required
def sticker(request, pk):
    order = get_object_or_404(Kvant, pk=pk)
    return render(request, 'sticker.html', {'order': order})


@login_required
def check_doc(request, pk):
    order = get_object_or_404(Transaction, pk=pk)
    return render(request, 'check_doc.html', {'order': order})

@login_required
def hand_in(request, pk):
    order = get_object_or_404(Kvant, pk=pk)
    return render(request, 'hand_in.html', {'order': order})

@login_required
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        posts = Kvant.objects.filter(Q(brand__icontains=q) | \
                                     Q(pk__icontains=q) | \
                                     Q(model_item__icontains=q) | \
                                     Q(customer__contact_name__icontains=q) | \
                                     Q(customer__phone__icontains=q) | \
                                     Q(status__icontains=q) | \
                                     Q(engineer__surname__icontains=q) | \
                                     Q(is_paid__icontains=q) | \
                                     Q(customer__email__icontains=q))
        return render_to_response('search.html', {'posts': posts, 'q': q})
    else:
        return render_to_response('search.html')

@login_required
def history(request):

    if request.method == "POST":

        customer_form = request.POST.get('customer_name', '')
        customer = Customer.objects.get(pk=customer_form)
        transactions = Transaction.objects.filter(agent=customer)


        if request.POST.get('save_button') is not None:


            if transactions.exists():

                try:
                   debit_sum = Decimal(transactions.aggregate(Sum('debit')).values()[0])
                   credit_sum = Decimal(transactions.aggregate(Sum('credit')).values()[0])
                except:
                   ValueError

            else:
                return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('kvant_base'), (u"Записи відсутні!")))

        elif request.POST.get('excel') is not None:

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("MyModel")


            columns = [
                (u"Номер замовлення"),
                (u"Дата"),
                (u"Вартість послуги"),
                (u"Витрата"),
                (u"Нотатки"),
            ]

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd.mm.yyyy'

            for i, fieldname in enumerate(columns):
                ws.write(0, i, fieldname)
                ws.col(i).width = 5000


            font_style = xlwt.XFStyle()
            font_style.alignment.wrap = 1


            row = 0
            for obj in transactions:
                row+= 1
                ws.write(row, 0, obj.order_number_id)
                ws.write(row, 1, obj.created_at, date_format)
                ws.write(row, 2, obj.debit)
                ws.write(row, 3, obj.credit)
                ws.write(row, 4, obj.notes)

            wb.save(response)
            return response


        else:
            return HttpResponseRedirect('/kvant_base')

        customer_balance = credit_sum - debit_sum

    return render(request, 'history.html', {'transactions': transactions, 'customer_balance': customer_balance, 'customer': customer})


@login_required
def assistant(request):
    tables = Kvant.objects.filter(Q(status='done') | Q(status='success') | Q(status='closed'), to_send='ASSISTANT', is_warranty=True, is_paid=False)

    return render(request, 'assistant.html', {'tables': tables})

@login_required
def assistant_done(request):
    tables = Kvant.objects.filter(Q(status='done') | Q(status='success') | Q(status='closed'), to_send='ASSISTANT', is_warranty=True, is_paid=True)

    return render(request, 'assistant.html', {'tables': tables})


@login_required
def assistant_doc(request):
    tables = Kvant.objects.filter(Q(status='done') | Q(status='success') | Q(status='closed'), to_send='ASSISTANT', is_warranty=True, is_paid=False)

    if request.method == "POST":

        if request.POST.get('save_button') is not None:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
            rb = xlrd.open_workbook(os.path.join(settings.DOC_FOLDER, 'assistant.xls'), on_demand=True,
                                    formatting_info=True)
            ws = rb.sheet_by_index(1)
            wb = copy(rb)
            ws = wb.get_sheet(1)

            if tables.exists():

                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd.mm.yyyy'

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1

                row = 0
                for obj in tables:
                    row += 1
                    ws.write(row, 0, obj.model_item)
                    ws.write(row, 2, obj.serial_number)
                    ws.write(row, 4, obj.warranty_start, date_format)
                    ws.write(row, 5, obj.date_now, date_format)
                    ws.write(row, 6, obj.customer.contact_name)
                    ws.write(row, 7, obj.customer.phone)
                    ws.write(row, 9, obj.reason)
                    ws.write(row, 14, obj.date_close, date_format)
                    ws.write(row, 15, obj.date_close, date_format)

                wb.save(response)

                for doc in tables:
                    doc.is_paid = True
                    doc.save()

    return response



@login_required
def photoservice_report(request):
    tables = Kvant.objects.filter(Q(status='success') | Q(status='closed'), to_send='PHOTORVICE_REPORT', is_warranty=True, is_paid=False)

    return render(request, 'photoservice_report.html', {'tables': tables})

@login_required
def photoservice_report_done(request):
    tables = Kvant.objects.filter(Q(status='success') | Q(status='closed'), to_send='PHOTORVICE_REPORT', is_warranty=True,      is_paid=True)

    return render(request, 'photoservice_report_done.html', {'tables': tables})


def photoservice_report_doc(request):

    tables = Kvant.objects.filter(Q(status='success') | Q(status='closed'), to_send='PHOTORVICE_REPORT',
                                  is_warranty=True, is_paid=False)

    if request.method == "POST":

        if request.POST.get('save_button') is not None:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
            rb = xlrd.open_workbook(os.path.join(settings.DOC_FOLDER, 'photo_report.xls'), on_demand=True,
                                    formatting_info=True)
            ws = rb.sheet_by_index(0)
            wb = copy(rb)
            ws = wb.get_sheet(0)

            if tables.exists():

                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd.mm.yyyy'

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1

                i = 0
                row = 0
                for obj in tables:
                    row += 1
                    i += 1
                    ws.write(row, 0, i)
                    ws.write(row, 1, u"%s %s" % (obj.brand, obj.model_item))
                    ws.write(row, 3, obj.serial_number)
                    ws.write(row, 4, obj.warranty_start, date_format)
                    ws.write(row, 6, obj.date_now, date_format)
                    ws.write(row, 7, obj.is_warranty)
                    ws.write(row, 8, obj.customer.contact_name)
                    ws.write(row, 9, u"Черновцы")
                    ws.write(row, 10, obj.customer.phone)
                    ws.write(row, 11, obj.reason)
                    ws.write(row, 12, u"акт на обмін")
                    ws.write(row, 13, obj.date_close, date_format)
                    ws.write(row, 14, u"4-02-1")
                    ws.write(row, 15, u"діагностика і виписка акту на обмін")


                wb.save(response)

                for doc in tables:
                    doc.is_paid = True
                    doc.save()

    return response


@login_required
def photoservice(request):
    tables = Kvant.objects.filter(to_send='PHOTORVICE', status='info')

    return render(request, 'photoservice.html', {'tables': tables})

@login_required
def photoservice_done(request):
    tables = Kvant.objects.filter(Q(status='success') | Q(status='closed') | Q(status='wait') | Q(status='done'), to_send='PHOTORVICE')

    return render(request, 'photoservice.html', {'tables': tables})


def photoservice_doc(request):

    tables = Kvant.objects.filter(to_send='PHOTORVICE', status='info')

    if request.method == "POST":

        if request.POST.get('save_button') is not None:

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=photo_service1.xls'
            rb = xlrd.open_workbook(os.path.join(settings.DOC_FOLDER, 'photo_service.xls'), on_demand=True,
                                    formatting_info=True)
            ws = rb.sheet_by_index(0)
            wb = copy(rb)
            ws = wb.get_sheet(0)

            if tables.exists():

                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd.mm.yyyy'

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1

                ws.write(2, 6, datetime.now(), date_format)
                i = 0
                row = 5
                for obj in tables:
                    row += 1
                    i += 1
                    ws.write(row, 0, i)
                    ws.write(row, 2, u"%s %s" % (obj.brand, obj.model_item))
                    ws.write(row, 3, obj.serial_number)
                    ws.write(row, 4, obj.warranty_start, date_format)
                    ws.write(row, 5, obj.is_warranty)
                    ws.write(row, 6, obj.look)
                    ws.write(row, 7, obj.reason)
                    ws.write(row, 9, obj.additional)
                    ws.write(row, 10, obj.notes)
                    ws.write(row, 11, obj.id)
                    ws.write(row, 13, obj.customer.contact_name)
                    ws.write(row, 15, obj.customer.phone)

                wb.save(response)

                for doc in tables:
                    doc.status = 'wait'
                    doc.save()

    return response

@login_required
def krok(request):

    tables = Kvant.objects.filter(to_send='KROK', status='info')

    return render(request, 'krok.html', {'tables': tables})

def krok_doc(request):

    tables = Kvant.objects.filter(to_send='KROK', status='info')

    if request.method == "POST":

        if request.POST.get('save_button') is not None:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
            rb = xlrd.open_workbook(os.path.join(settings.DOC_FOLDER, 'Krok.xls'), on_demand=True, formatting_info=True)
            ws = rb.sheet_by_index(0)
            wb = copy(rb)
            ws = wb.get_sheet(0)

            if tables.exists():

                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd.mm.yyyy'

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1


                i = 0
                row = 0
                for obj in tables:
                    row += 1
                    i += 1
                    ws.write(row, 0, i)
                    ws.write(row, 1, u"Квант сервис")
                    ws.write(row, 2, u"Черновцы")
                    ws.write(row, 3, obj.id)
                    ws.write(row, 4, obj.warranty_start, date_format)
                    ws.write(row, 5, obj.date_now, date_format)
                    ws.write(row, 6, obj.is_warranty)
                    ws.write(row, 7, obj.brand)
                    ws.write(row, 8, obj.model_item)
                    ws.write(row, 9, obj.serial_number)
                    ws.write(row, 10, u"%s %s" % (obj.customer.contact_name, obj.customer.phone))
                    ws.write(row, 11, obj.reason)
                    ws.write(row, 12, obj.additional)
                    ws.write(row, 14, obj.notes)

                wb.save(response)

                for doc in tables:
                    doc.status = 'wait'
                    doc.save()

    return response




@login_required
def paid_engineer_report(request, pk):

    repairs = SalaryReport.objects.filter(is_paid=True, engineer__pk__in=pk)

    if request.method == "POST":

        if request.POST.get('save_button') is not None:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=mymodel.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("MyModel")

            if repairs.exists():


                columns = [
                    (u"Номер замовлення"),
                    (u"Дата"),
                    (u"Бренд"),
                    (u"Модель"),
                    (u"Вартість"),
                    (u"Інженер"),
                    (u"Вид роботи"),
                    (u"Вартість роботи"),
                ]

                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd.mm.yyyy'

                for i, fieldname in enumerate(columns):
                    ws.write(0, i, fieldname)
                    ws.col(i).width = 5000

                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1

                row = 0
                for obj in repairs:
                    row += 1
                    ws.write(row, 0, obj.repair.pk)
                    ws.write(row, 1, obj.paid_date, date_format)
                    ws.write(row, 2, obj.repair.brand)
                    ws.write(row, 3, obj.repair.model_item)
                    ws.write(row, 4, obj.repair_cost)
                    ws.write(row, 5, obj.engineer.nickname)
                    ws.write(row, 6, obj.item.name)
                    if obj.paid_engineer > 0:
                        ws.write(row, 7, obj.paid_engineer)
                    else:
                        ws.write(row, 7, obj.item.paid_engineer)

                wb.save(response)
            else:
                return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('paid_engineer', args=(pk,)), (u"Записи відсутні!")))

    return response

class LoginRequiredMixin(object):

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AddOrder(LoginRequiredMixin, CreateView):
    model = Kvant
    template_name = 'add_order.html'
    form_class = AddOrderForm

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            return HttpResponse(
                u'%s?status_message=Скасовано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
        else:
            return super(AddOrder, self).post(request, *args, **kwargs)

    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(AddOrder, self).form_invalid(form)

    def get_success_url(self):

        return reverse('edit_order', args=(self.object.pk,))



class AddCustomer(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'add_customer.html'
    form_class = AddCustomerForm

    def form_valid(self, form):

        response = super(AddCustomer, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'contact_name': self.object.contact_name,
                'phone': self.object.phone,
                'email': self.object.email,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(AddCustomer, self).form_invalid(form)

    def get_success_url(self):

        return reverse('add_customer')

class EditCustomer(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'edit_customer.html'

    form_class = AddCustomerForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponse(
                u'%s?status_message=Скасовано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
        else:
            return super(EditCustomer, self).post(request, *args, **kwargs)

    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(EditCustomer, self).form_invalid(form)


    def get_success_url(self):
        return reverse('edit_customer', args=(self.object.pk,))



class EditOrder(LoginRequiredMixin, UpdateView):
    model = Kvant
    template_name = 'edit_order.html'

    form_class = AddOrderForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponse(
                u'%s?status_message=Скасовано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
        else:
            return super(EditOrder, self).post(request, *args, **kwargs)

    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(EditOrder, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(EditOrder, self).get_context_data(**kwargs)
        queryset_paid = SalaryReport.objects.filter(repair=self.object.pk)
        context['reports'] = queryset_paid
        order = Kvant.objects.get(pk=self.object.pk)
        context['customer'] = order.customer
        if queryset_paid.exists():
            context['cost_repair'] = queryset_paid.aggregate(Sum('repair_cost')).values()[0]
        else:
            context['cost_repair'] = 0

        return context

    def get_success_url(self):
        return reverse('edit_order', args=(self.object.pk,))


class AddSalaryReport(LoginRequiredMixin, CreateView):
    model = SalaryReport
    template_name = 'salary_report.html'
    form_class = SalaryReportForm

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            return HttpResponse(
                u'%s?status_message=Скасовано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
        else:
            return super(AddSalaryReport, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)
        report.repair = Kvant.objects.get(id=self.kwargs['pk'])

        return super(AddSalaryReport, self).form_valid(form)


    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(AddSalaryReport, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddSalaryReport, self).get_context_data(**kwargs)
        context['repair'] = self.kwargs['pk']

        return context

    def get_success_url(self):

        return reverse('salary_report', args=(self.object.pk,))

class EditSalaryReport(LoginRequiredMixin, UpdateView):
    model = SalaryReport
    template_name = 'edit_salary_report.html'

    form_class = SalaryReportForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponse(
                u'%s?status_message=Скасовано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
        else:
            return super(EditSalaryReport, self).post(request, *args, **kwargs)

    def form_invalid(self, form):

        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          mimetype="application/json")
        return super(EditSalaryReport, self).form_invalid(form)

    def get_success_url(self):
        return reverse('edit_salary_report', args=(self.object.pk,))

class DeleteSalaryReport(LoginRequiredMixin, DeleteView):
    model = SalaryReport
    template_name = 'salary_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Роботу успішно видалено!' \
            % reverse('kvant_base')

@login_required
def copy_order(request, pk):
    new_order = Kvant.objects.get(pk=pk)

    if request.method == "POST":

        if request.POST.get('save_button') is not None:
            new_order.pk = None
            new_order.status = 'accept'
            new_order.date_close = None
            new_order.save()
        return HttpResponse(
            '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
    return render(request, 'copy_order.html', {'new_order': new_order})



@login_required
def close_order(request, pk):
    order = Kvant.objects.get(pk=pk)
    income = Transaction.objects.all()
    balances = Balance.objects.all()

    if request.method == "POST":

        if request.POST.get('save_button') is not None:

            errors = {}

            ord = Kvant.objects.get(pk=pk)

            balance = request.POST.get('balance_name', '')
            is_money = request.POST.get('is_money', None)

            if not balance:
                errors['balance'] = u"Оберіть касу"
            else:
                balance = Balance.objects.get(pk=balance)

            try:
                cost_repair = Decimal(request.POST.get('cost_repair', '').strip())
            except:
                ValueError

            if ord.status != 'closed':
                ord.close_order()
                ord.save()
                if cost_repair != 0:
                    income = Transaction(balance=balance, debit=cost_repair,
                                     order_number=Kvant.objects.get(pk=pk), agent=ord.customer)
                    income.save()
                    balance.balance_debit(debit=income.debit)


            else:
                return HttpResponse('Замовлення вже закрите')

            return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

        elif request.POST.get('cancel_button') is not None:
            return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

    return render(request, 'close_order.html', {'order': order, 'income': income, 'balances': balances})

@login_required
def add_debit(request):
    form_class = AddDebitForm
    form = form_class(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            debit = form.cleaned_data['debit']
            balance=form.cleaned_data['balance']
            balance.balance_debit(debit)
            form.save()
            return HttpResponse(
                u'%s?status_message=Клієнта додано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

    return render(request, 'debit.html', {'form': form})

@login_required
def edit_debit(request, pk):

    transaction = get_object_or_404(Transaction, pk=pk)
    debit = transaction.debit
    balance = transaction.balance
    form_class = AddDebitForm
    form = form_class(request.POST or None, instance=transaction)

    if request.method == 'POST':

        if form.is_valid():

            new_debit = Decimal(form.cleaned_data['debit'])
            setattr(transaction, 'debit', new_debit)

            balance.current_balance = (balance.current_balance + new_debit) - debit

            balance.save()

            form.save()

            return HttpResponse(u'%s?status_message=Клієнта додано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

    return render(request, 'edit_debit.html', {'form': form, 'transaction': transaction})

@login_required
def edit_credit(request, pk):

    transaction = get_object_or_404(Transaction, pk=pk)
    credit = transaction.credit
    balance = transaction.balance
    form_class = AddCreditForm
    form = form_class(request.POST or None, instance=transaction)

    if request.method == 'POST':

        if form.is_valid():

            new_credit = Decimal(form.cleaned_data['credit'])
            setattr(transaction, 'credit', new_credit)

            balance.current_balance = (balance.current_balance - new_credit) + credit

            balance.save()

            form.save()

            return HttpResponse(u'%s?status_message=Клієнта додано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

    return render(request, 'edit_credit.html', {'form': form, 'transaction': transaction})

@login_required
def add_credit(request):

    form_class = AddCreditForm
    form = form_class(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            credit = Decimal(form.cleaned_data['credit'])
            balance = form.cleaned_data['balance']
            balance.balance_credit(credit)
            form.save()
            return HttpResponse(
                u'%s?status_message=Клієнта додано!' % '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

    return render(request, 'credit.html', {'form': form})

