import math

class MortgageCalculator:

    def __init__(self, principal, interest, years):
        self.principal = principal
        self.interest = interest
        self.years = years

    def payments(self):
        # monthly rate from annual percentage rate
        interest_rate = float(self.interest)/(100.0 * 12.0)
        # total number of payments
        payment_num = int(self.years) * 12
        # calculate monthly payment
        payment = float(self.principal) * (interest_rate/(1-math.pow((1+interest_rate), (-payment_num))))
        return payment
