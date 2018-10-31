import math

class MortgageCalculator:

    def __init__(self, principal, interest, years):
        self.principal = principal
        self.interest = interest
        self.years = years

    def payments(self):
        # monthly rate from annual percentage rate
        interest_rate = self.interest/(100 * 12)
        # total number of payments
        payment_num = self.years * 12
        # calculate monthly payment
        payment = self.principal * \
            (interest_rate/(1-math.pow((1+interest_rate), (-payment_num))))
        return payment


# mortgage loan principal
principal = 100000
# percent annual interest
interest = 7.5
# years to pay off mortgage
years = 30

mortgage_calc = MortgageCalculator(principal, interest, years)

# calculate monthly payment amount
monthly_payment = mortgage_calc.payments()
# calculate total amount paid
total_amount = monthly_payment * years * 12
# show result ...
# {:,} uses the comma as a thousands separator
sf = '''\
For a {} year mortgage loan of ${:,}
at an annual interest rate of {:.2f}%
you pay ${:.2f} monthly'''
print(sf.format(years, principal, interest, monthly_payment))
print('-'*40)
print("Total amount paid will be ${:,.2f}".format(total_amount))
''' result ...
For a 30 year mortgage loan of $100,000
at an annual interest rate of 7.50%
you pay $699.21 monthly
----------------------------------------
Total amount paid will be $251,717.22
'''
