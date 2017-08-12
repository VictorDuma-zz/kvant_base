# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import BadHeaderError


from models import Repair
from models import Warranty
from models import Certificate
from forms import ContactForm

from django.conf import settings

if "django_mailer" in settings.INSTALLED_APPS:
    from django_mailer import send_mail
else:
    from django.core.mail import send_mail


# Create your views here.
def my_site(request):

    warrantys = Warranty.objects.all()
    repairs = Repair.objects.all()
    certificates = Certificate.objects.all()

    #feedback logic
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recepients = ['kvant.cv@gmail.com']

            if copy:
                recepients.append(sender)
            try:
                send_mail(subject, message, sender, recepients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')

            return HttpResponseRedirect('#contacts')

    else:
        form = ContactForm()

    return render(request, 'index.html', {'repairs': repairs, 'warrantys': warrantys, 'certificates': certificates, 'form': form})
