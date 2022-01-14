from django.contrib import admin
from . import models

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id','company_name', 'funds']
    list_per_page = 50

@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id','company','employee_name', 'card_type', 'available_balance']
    list_per_page = 50


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id','restaurant_name']
    list_per_page = 50

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','card','restaurant','transaction_name', 'transaction_date', 'transaction_type', 'amount']
    list_per_page = 50

