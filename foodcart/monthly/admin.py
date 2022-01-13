from django.contrib import admin
from . import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'funds']
    list_per_page = 50

@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['company','employee_name', 'card_type', 'available_balance']
    list_per_page = 50


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['company','card','transaction_name', 'transaction_date', 'transaction_type', 'amount']
    list_per_page = 50
