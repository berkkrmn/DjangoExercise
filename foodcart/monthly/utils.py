from django.db import transaction
from django.db.models import Q, Count, Sum
from monthly.models import Company, Card, Transaction, Restaurant

CITY_CENTER_CARD_TOP_UP = 500
SMALL_TOWN_CARD_TOP_UP = 300

# Function -> Create a new company.
# Parameters:
#   company_name = string 
def create_company(company_name):
    try:
        Company.objects.create(company_name=company_name)
        return company_name + ' is created.'
    except Exception as e: 
        return str(e)

# Function -> Create a new card for a company.
# Parameters:
#   company_id = integer
#   employee_name = string
#   contract_type = string -> Accepts 'S' or 'C' as values.
def create_card(company_id, employee_name, contract_type):
    if contract_type == 'S' | contract_type == 'C':
        try:
            company = Company.objects.get(pk=company_id)
            Card.objects.create(company=company, employee_name=employee_name, card_type=contract_type)
            if contract_type == 'C':
                return 'Created City Center Card for ' + company.company_name + ' - '+ employee_name
            else:
                return 'Created Small Town Card for ' + company.company_name + ' - '+ employee_name
        except Exception as e:
            return str(e) 
    else:
        return 'Invalid contract_type.'
        
# Function -> Get the list of cards of a company.
# Parameters:
#   company_id = integer
def get_list_of_cards(company_id):
    try:
        company = Company.objects.get(pk=company_id)
        query_set = Card.objects.filter(company=company).values()
        list_of_cards = list(query_set)
        if len(list_of_cards) == 0:
            return 'No cards were found for the company ' + company.company_name
        else:
            return list_of_cards
    except Exception as e:
        return str(e)

# Function -> Add funds to a company.
# Parameters:
#   company_id = integer
#   funds = double    
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

# Function -> Get available spending balance of a card.
# Parameters:
#   card_id = integer
def get_available_balance(card_id):
    try:
        card = Card.objects.get(pk=card_id)
        return card.available_balance
    except Exception as e:
        return str(e)

# Function -> Top-Up a card balance.
# Parameters:
#    card_id = integer
def top_up(card_id):
    try:
        card = Card.objects.get(pk=card_id)
        company = card.company

        # This process is atomic in order to prevent errors. The process as follows:
        # 1) Set card balance according to card type. Also check if company has enough funds to make this operation.
        # 2) Subtract the new card balance from company funds.
        # 3) Save card, save company.
        # 4) If both succeed, create a transaction as a Top-Up for this card.
        with transaction.atomic():
            if (card.card_type == 'C') & (company.funds >= CITY_CENTER_CARD_TOP_UP):
                card.available_balance = CITY_CENTER_CARD_TOP_UP
                company.funds = company.funds - CITY_CENTER_CARD_TOP_UP
                card.save()
                company.save()

                Transaction.objects.create(company=company, card=card, amount=CITY_CENTER_CARD_TOP_UP, transaction_type='T', transaction_name='Top-Up')
                return card.employee_name + ' card balance updated to ' + str(CITY_CENTER_CARD_TOP_UP)
            elif (card.card_type == 'S') & (company.funds >= SMALL_TOWN_CARD_TOP_UP):
                card.available_balance = SMALL_TOWN_CARD_TOP_UP
                company.funds = company.funds - SMALL_TOWN_CARD_TOP_UP
                card.save()
                company.save()
                
                Transaction.objects.create(company=company, card=card, amount=SMALL_TOWN_CARD_TOP_UP, transaction_type='T', transaction_name='Top-Up')
                return card.employee_name + ' card balance updated to ' + str(SMALL_TOWN_CARD_TOP_UP)
            else:
                return 'Not enough funds.'
    except Exception as e:
        return str(e)

# Function -> Spend money on a restaurant with a card.
# Parameters:
#   card_id = integer
#   spend_amount = double
#   restaurant_id = integer
def spend_money(card_id, spend_amount, restaurant_id):
    try:
        card = Card.objects.get(pk=card_id)
        company = card.company
        restaurant = Restaurant.objects.get(pk=restaurant_id)

        if card.available_balance < spend_amount:
            return 'Not enough balance.'
        else:
            card.available_balance = card.available_balance - spend_amount
            card.save()

            Transaction.objects.create(company=company, card=card, restaurant=restaurant, amount=spend_amount, transaction_type='P', transaction_name=restaurant.restaurant_name)
            return card.employee_name + ' spend ' + str(spend_amount) + ' at ' + restaurant.restaurant_name

    except Exception as e:
        return str(e)

# Function -> Refund a purchase.
# Parameters:
#   transaction_id = integer
def refund_purchase(transaction_id):
    try:
        # Get purchase information.
        refund_transaction = Transaction.objects.get(pk=transaction_id)
        card = refund_transaction.card

        # Transaction must be purchase.
        if refund_transaction.transaction_type != 'P':
            return 'Transaction is not a purchase.'
        else:
            # Refund the amount to the card.
            card.available_balance = card.available_balance + refund_transaction.amount
            card.save()

            # Convert purchase into a refund.
            refund_transaction.transaction_type = 'R'
            refund_transaction.save()

            return str(refund_transaction.amount) + ' is refunded to ' + card.employee_name
    except Exception as e:
        return str(e)

# Function -> Get the list of all transactions of a card.
# Parameters:
#   card_id = integer
def get_list_of_transactions(card_id):
    try:
        # Get all transactions for the card. (Top-Ups and Purchases. Refunds can also be added if requested).
        # Return if the card has at least one transaction recorded.
        card = Card.objects.get(pk=card_id)
        transactions_list = list(Transaction.objects.filter(card=card).filter(Q(transaction_type='T') | Q(transaction_type='P')).values())
        if len(transactions_list) == 0:
            return 'No transactions found.'
        else:
            return transactions_list
    except Exception as e:
        return str(e)

# Function -> Get the list of most popular restaurants per month for a company.
# Parameters:
#   company_id = integer
#   month = integer -> Accepts values between 1 to 12.
def most_popular_restaurants(company_id, month):
    try:
        company = Company.objects.get(pk=company_id)
        restaurants = Transaction.objects.filter(company=company).filter(transaction_date__month=month).filter(transaction_type='P').values('restaurant__restaurant_name').annotate(purchase_count=Count('restaurant'), total_amount=Sum('amount')).order_by('-purchase_count')    
        popular_rest_list = list(restaurants)
        if len(popular_rest_list) == 0:
            return 'No purchases are found for ' + company.company_name
        else:
            return popular_rest_list
    except Exception as e:
        return str(e)
    
# Function -> Terminate a card.
# Parameters:
#   card_id = integer
def terminate_card(card_id):
    try:
        # Delete the card object and refund its balance to the company.
        # The transaction foreign keys of the card will be set to null so that the transactions are not lost.
        card = Card.objects.get(pk=card_id)
        company = card.company
        company.funds = company.funds + card.available_balance
        company.save()
        card.delete()

        return 'Card deleted successfully.'
    except Exception as e:
        return str(e)