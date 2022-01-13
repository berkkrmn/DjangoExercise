from django.db import transaction
from monthly.models import Company, Card, Transaction


def create_company(company_name):
    try:
        Company.objects.create(company_name=company_name)
        return company_name + ' is created.'
    except Exception as e: 
        return str(e)

def create_card(company, employee_name, contract_type):
    try:
        Card.objects.create(company=company, employee_name=employee_name, card_type=contract_type)
        if contract_type == 'C':
            return 'Created City Center Card for ' + employee_name
        else:
            return 'Created Small Town Card for ' + employee_name
    except Exception as e:
        return str(e)

def get_list_of_cards(company_id):
    try:
        company = Company.objects.get(pk=company_id)
        query_set = Card.objects.filter(company=company).values()
        list_of_cards = list(query_set)
        if len(list_of_cards) == 0:
            return 'No cards were found for the company ' + company.company_name
        else:
            return str(list_of_cards)
    except Exception as e:
        return str(e)
    
def add_funds(company_id, funds):
    if funds <= 0:
        return 'Invalid funds.'
    else: 
        try:
            company = Company.objects.get(pk=company_id)
            updated_funds = funds + company.funds
            company.funds = updated_funds
            company.save()
            return str(funds) + ' funds have been added to ' + company.company_name
        except Exception as e:
            return str(e)

def get_available_balance(card_id):
    try:
        card = Card.objects.get(pk=card_id)
        return str(card.available_balance)
    except Exception as e:
        return str(e)

def top_up(card_id):
    try:
        card = Card.objects.get(pk=card_id)
        company = card.company

        with transaction.atomic():
            if (card.card_type == 'C') & (company.funds > 500):
                card.available_balance = 500
                company.funds = company.funds - 500
                card.save()
                company.save()

                Transaction.objects.create(company=company, card=card, amount=500, transaction_type='T', transaction_name='Top-Up')
                return card.employee_name + ' card balance updated to 500.'
            elif (card.card_type == 'S') & (company.funds > 300):
                card.available_balance = 300
                company.funds = company.funds - 300
                card.save()
                company.save()
                
                Transaction.objects.create(company=company, card=card, amount=300, transaction_type='T', transaction_name='Top-Up')
                return card.employee_name + ' card balance updated to 300.'
            else:
                return 'Not enough funds.'
    except Exception as e:
        return str(e)

def spend_money(card_id, spend_amount, restaurant_name):
    try:
        card = Card.objects.get(pk=card_id)
        company = card.company

        if card.available_balance < spend_amount:
            return 'Not enough balance.'
        else:
            card.available_balance = card.available_balance - spend_amount
            card.save()

            Transaction.objects.create(company=company, card=card, amount=spend_amount, transaction_type='P', transaction_name=restaurant_name)
            return card.employee_name + ' spend ' + str(spend_amount) + ' at ' + restaurant_name

    except Exception as e:
        return str(e)