# -*- coding:utf-8 -*-


from django.conf.urls import patterns
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG
from kvant_crm.views import AddCustomer, AddOrder, EditOrder, ListCustomers, PaidEngineer, ListPaid, AddSalaryReport, EditCustomer, EditSalaryReport, DeleteSalaryReport
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [

    url(r'^$', 'my_site.views.my_site', name='my_site'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^kvant_base$', 'kvant_crm.views.kvant_base', name='kvant_base'),
    url(r'^kvant_base/assistant$', 'kvant_crm.views.assistant', name='assistant'),
    url(r'^kvant_base/assistant_doc$', 'kvant_crm.views.assistant_doc', name='assistant_doc'),
    url(r'^kvant_base/assistant_done$', 'kvant_crm.views.assistant_done', name='assistant_done'),
    url(r'^kvant_base/krok$', 'kvant_crm.views.krok', name='krok'),
    url(r'^kvant_base/krok_doc$', 'kvant_crm.views.krok_doc', name='krok_doc'),
    url(r'^kvant_base/photoservice$', 'kvant_crm.views.photoservice', name='photoservice'),
    url(r'^kvant_base/photoservice_done$', 'kvant_crm.views.photoservice_done', name='photoservice_done'),
    url(r'^kvant_base/photoservice_doc$', 'kvant_crm.views.photoservice_doc', name='photoservice_doc'),
    url(r'^kvant_base/photoservice_report$', 'kvant_crm.views.photoservice_report', name='photoservice_report'),
    url(r'^kvant_base/photoservice_report_doc$', 'kvant_crm.views.photoservice_report_doc', name='photoservice_report_doc'),
    url(r'^kvant_base/photoservice_report_done$', 'kvant_crm.views.photoservice_report_done', name='photoservice_report_done'),
    url(r'^kvant_base/finance$', 'kvant_crm.views.finance', name='finance'),
    url(r'^kvant_base/search/$', 'kvant_crm.views.search', name='search'),
    url(r'^kvant_base/(?P<pk>\d+)/paid_engineer/$', PaidEngineer.as_view(), name='paid_engineer'),
    url(r'^kvant_base/(?P<pk>\d+)/paid_engineer_report/$', 'kvant_crm.views.paid_engineer_report', name='paid_engineer_report'),
    url(r'^kvant_base/paid_list/$', ListPaid.as_view(), name='paid_list'),
    url(r'^kvant_base/history/$', 'kvant_crm.views.history', name='history'),
    url(r'^kvant_base/add_order/$', AddOrder.as_view(), name='add_order'),
    url(r'^kvant_base/(?P<pk>\d+)/salary_report/$', AddSalaryReport.as_view(), name='salary_report'),
    url(r'^kvant_base/(?P<pk>\d+)/edit_salary_report/$', EditSalaryReport.as_view(), name='edit_salary_report'),
    url(r'^kvant_base/(?P<pk>\d+)/salary_confirm_delete/$', DeleteSalaryReport.as_view(), name='salary_confirm_delete'),
    url(r'^kvant_base/(?P<pk>\d+)/copy_order/$', 'kvant_crm.views.copy_order', name='copy_order'),
    url(r'^kvant_base/customer_list/$', ListCustomers.as_view(), name='customer_list'),
    url(r'^kvant_base/add_customer/$', AddCustomer.as_view(), name='add_customer'),
    url(r'^kvant_base/(?P<pk>\d+)/edit_order/$', EditOrder.as_view(), name='edit_order'),
    url(r'^kvant_base/(?P<pk>\d+)/edit_customer/$', EditCustomer.as_view(), name='edit_customer'),
    url(r'^kvant_base/finance/(?P<pk>\d+)/edit_debit/$', 'kvant_crm.views.edit_debit', name='edit_debit'),
    url(r'^kvant_base/finance/(?P<pk>\d+)/edit_credit/$', 'kvant_crm.views.edit_credit', name='edit_credit'),
    url(r'^kvant_base/finance/debit/$', 'kvant_crm.views.add_debit', name='debit'),
    url(r'^kvant_base/finance/credit/$', 'kvant_crm.views.add_credit', name='credit'),
    url(r'^kvant_base/(?P<pk>\d+)/close_order/$', 'kvant_crm.views.close_order', name='close_order'),
    url(r'^kvant_base/(?P<pk>\d+)/order_doc/$', 'kvant_crm.views.order_doc', name='order_doc'),
    url(r'^kvant_base/(?P<pk>\d+)/sticker/$', 'kvant_crm.views.sticker', name='sticker'),
    url(r'^kvant_base/(?P<pk>\d+)/hand_in/$', 'kvant_crm.views.hand_in', name='hand_in'),
    url(r'^kvant_base/finance/(?P<pk>\d+)/check_doc/$', 'kvant_crm.views.check_doc', name='check_doc'),
    url(r'^admin/', admin.site.urls),

]

if DEBUG:

    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': MEDIA_ROOT}))


