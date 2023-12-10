from django.db import models
from datetime import datetime
from decimal import Decimal


class Trades(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=50)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.CharField(max_length=100)

    def daily_interest_rate(self):
        interest_rate = float(self.interest_rate.strip('%'))
        daily_interest_rate_percent = interest_rate / 100
        daily_interest_rate = daily_interest_rate_percent / 365

        return daily_interest_rate

    def daily_interest_amount(self):
        funding = self.cashflows.filter(cashflow_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)
        daily_interest_rate = Decimal(self.daily_interest_rate())
        return invested_amount * daily_interest_rate

    def passed_days(self, reference_date):
        reference_date_value = datetime.strptime(reference_date, "%Y-%m-%d").date()
        return (reference_date_value - self.investment_date).days

    def gross_expected_interest_amount(self, reference_date):

        return self.daily_interest_amount() * self.passed_days(reference_date)

    def gross_expected_amount(self, reference_date):
        funding = self.cashflows.filter(cashflow_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)

        return invested_amount + self.gross_expected_interest_amount(reference_date)

    def realized_amount(self, reference_date):
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
        repayment_values = self.cashflows.filter(cashflow_type='repayment', cashflow_date__lte=reference_date)
        realized_amount = sum([cashflow.amount for cashflow in repayment_values])
        return realized_amount

    def remaining_invested_amount(self, reference_date):
        funding = self.cashflows.filter(cashflow_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)
        return invested_amount - self.realized_amount(reference_date)

    def get_closing_date(self):
        trades = self.cashflows.filter(trade_id=self.loan_id)
        date = ""
        realized = 0
        to_pay = 0
        for trade in trades:
            if trade.cashflow_type == "repayment":
                realized += trade.amount
                date = str(trade.cashflow_date)
            if trade.cashflow_type == "funding":
                to_pay = self.gross_expected_amount(str(self.maturity_date))
            if realized > to_pay:
                return f"The loan is closed in : {date}"

        return f"The loan is not closed. The loan was supposed to close in : {self.maturity_date}, but the realized amount was down for {(to_pay - realized):.2f}"


class Cash_flows(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=50)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE, db_column='loan_id', related_name="cashflows")
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=100)
    cashflow_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.
