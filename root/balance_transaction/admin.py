from django.contrib import admin

from .models import *


@admin.register(Wallet)
class Wallet(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    pass

@admin.register(TransactionType)
class TransactionType(admin.ModelAdmin):
    pass