from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class User(models.Model):
    PROVIDER = 'PR'
    CUSTOMER = 'CU'
    BANK = 'BK'
    TYPES_CHOICES = [
        (PROVIDER, 'Loan Provider'),
        (CUSTOMER, 'Loan Customer'),
        (BANK, 'Junior'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    # FOR TYPES: 0 => Loan Provider, 1 => Loan Customer, 2 => Bank
    type = models.CharField(max_length=2, choices=TYPES_CHOICES)
    password = models.CharField(max_length=150 )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class LoanFund(models.Model):
    LOAN = 'LN'
    FUND = 'FD'
    TYPES_CHOICES = [
        (LOAN, 'Loan'),
        (FUND, 'Loan Fund'),
    ]
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    min_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=3)
    type = models.CharField(max_length=2, choices=TYPES_CHOICES)      #True ==> Loan   |   False ==> Fund


    def __str__(self):
        return f"{self.name}, Interest Rate: {self.interest_rate}"


class Application(models.Model):
    APPROVED = 'AV'
    PENDING = 'PD'
    REJECTED = 'RJ'
    TYPES_CHOICES = [
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
    ]
    start_date = models.DateTimeField()
    status = models.CharField(max_length=2, choices=TYPES_CHOICES)  #True ==> Accepted   |   False ==> Pending
    loan_fund = models.ForeignKey(LoanFund, on_delete=models.PROTECT, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="applications")

    def get_status(self):
        return "Accepted" if self.status else "Pending"

    def __str__(self):
        return f"{self.user.full_name()}, Loan/Fund Name: {self.loan_fund.name}, Status: {self.get_status()}"


class Payment(models.Model):
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date = models.DateTimeField()
    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name="payments")

