from django.db import models
from django.db.models.fields.related import ForeignKey

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    funds = models.DecimalField(max_digits=11, decimal_places=2)

class Card(models.Model):
    CARD_TYPE_CITY_CENTER = 'C'
    CARD_TYPE_SMALL_TOWN = 'S'

    CARD_TYPES = [ 
        (CARD_TYPE_CITY_CENTER, 'City Center'),
        (CARD_TYPE_SMALL_TOWN, 'Small Town')
    ]

    company = ForeignKey(Company, on_delete=models.CASCADE)
    available_balance = models.DecimalField(max_digits=5, decimal_places=2)
    card_type = models.CharField(max_length=1, choices=CARD_TYPES)
    employee_name = models.CharField(max_length=255)

class Transaction(models.Model):
    TRANSACTION_TOP_UP = 'T'
    TRANSACTION_PURCHASE = 'P'
    TRANSACTION_REFUND = 'R'

    TRANSACTION_TYPES = [
        (TRANSACTION_TOP_UP, 'Top-Up'),
        (TRANSACTION_PURCHASE, 'Purchase'),
        (TRANSACTION_REFUND, 'Refund')
    ]

    # default is set to "company" if a card is deleted. 
    # Because we would want to see all transactions of a card even if it's deleted.
    card = ForeignKey(Card, on_delete=models.SET_DEFAULT, default='company')
    
    company = ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    restaurant = models.CharField(max_length=255, null=True)
