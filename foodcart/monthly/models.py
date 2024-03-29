from django.db import models
from django.db.models.fields.related import ForeignKey

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    funds = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return self.company_name

    class Meta:
        ordering = ['company_name']

class Card(models.Model):
    CARD_TYPE_CITY_CENTER = 'C'
    CARD_TYPE_SMALL_TOWN = 'S'

    CARD_TYPES = [ 
        (CARD_TYPE_CITY_CENTER, 'City Center'),
        (CARD_TYPE_SMALL_TOWN, 'Small Town')
    ]

    company = ForeignKey(Company, on_delete=models.CASCADE)
    available_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    card_type = models.CharField(max_length=1, choices=CARD_TYPES)
    employee_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.employee_name
        
    class Meta:
        ordering = ['employee_name']

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.restaurant_name

    class Meta:
        ordering = ['restaurant_name']

class Transaction(models.Model):
    TRANSACTION_TOP_UP = 'T'
    TRANSACTION_PURCHASE = 'P'
    TRANSACTION_REFUND = 'R'

    TRANSACTION_TYPES = [
        (TRANSACTION_TOP_UP, 'Top-Up'),
        (TRANSACTION_PURCHASE, 'Purchase'),
        (TRANSACTION_REFUND, 'Refund')
    ]

    company = ForeignKey(Company, on_delete=models.CASCADE)
    card = ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    restaurant = ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    transaction_name = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.transaction_name

    class Meta:
        ordering = ['company']

