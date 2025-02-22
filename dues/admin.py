from django.contrib import admin

from dues.models import BankAccount, DuesEntry, DuesPayPeriod, Transaction

admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(DuesPayPeriod)
admin.site.register(DuesEntry)
