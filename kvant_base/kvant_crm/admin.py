from django.contrib import admin

from models import Customer, Engineer, Kvant, Transaction, Balance, KindRepair


admin.site.register(Kvant)
admin.site.register(Customer)
admin.site.register(Engineer)
admin.site.register(Transaction)
admin.site.register(Balance)
admin.site.register(KindRepair)
