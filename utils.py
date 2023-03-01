from datetime import datetime, timedelta
import random
from models import Customer, Account, Transaction
import barnum

def check_valid_withdraw(balance, amount):
    new_balance = balance - amount
    if amount > balance or new_balance < 0 or amount <= 0:
        raise Exception('Invalid amount.')

def seed_data(db):
    customer_count = Customer.query.count()
    while customer_count < 5000:
        customer = Customer()
        customer.first_name, customer.last_name = barnum.create_name()
        customer.street_address = barnum.create_street()
        customer.zipcode, customer.city, _  = barnum.create_city_state_zip()
        customer.country = "USA"
        customer.country_code = "US"
        customer.birthday = barnum.create_birthday()
        n = barnum.create_cc_number()
        customer.national_id = customer.birthday.strftime("%Y%m%d-") + n[1][0][0:4]
        customer.telephone_country_code = 55
        customer.telephone = barnum.create_phone()
        customer.email_address = barnum.create_email().lower()

        for x in range(1, 4):
            account = Account()

            c = random.randint(0, 100)
            if c < 33:
                account.account_type = 'Personal'
            elif c < 66:
                account.account_type = 'Checking'
            else:
                account.account_type = 'Savings'
            
            random_date = datetime(1990, 5, 17) + timedelta(days=random.randint(1000, 10000))
            account.created = random_date
            account.balance = 0

            for n in range(random.randint(0, 30)):
                balance = random.randint(0, 30) * 100
                transaction = Transaction()
                random_date = random_date + timedelta(days=random.randint(10,100))
                if random_date > datetime.now():
                    break
                transaction.date = random_date
                account.transactions.append(transaction)
                transaction.amount = balance
                if account.balance - balance < 0:
                    transaction.type = 'Debit'
                else:
                    if random.randint(0, 100) > 70:
                        transaction.type = 'Debit'
                    else:
                        transaction.type = 'Credit'
                
                r = random.randint(0, 100)
                if transaction.type == "Debit":
                    account.balance = account.balance + balance
                    if r < 20:
                        transaction.operation = "Deposit cash"
                    elif r < 66:
                        transaction.operation = "Salary"
                    else:
                        transaction.operation = "Transfer"
                else:
                    account.balance = account.balance - balance
                    if r < 40:
                        transaction.operation = "ATM withdrawal"
                    if r < 75:
                        transaction.operation = "Payment"
                    elif r < 85:
                        transaction.operation = "Bank withdrawal"
                    else:
                        transaction.operation = "Transfer"

                transaction.new_balance = account.balance

            customer.accounts.append(account)
        
        db.session.add(customer)
        db.session.commit()
        customer_count += 1
