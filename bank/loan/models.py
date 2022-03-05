from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.



class LoanFund(models.Model):
    LOAN = 'LN'
    FUND = 'FD'
    TYPES_CHOICES = [
        (LOAN, 'Loan'),
        (FUND, 'Loan Fund'),
    ]
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    min_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=3)
    type = models.CharField(max_length=2, choices=TYPES_CHOICES)      #True ==> Loan   |   False ==> Fund


    def __str__(self):
        types = dict(self.TYPES_CHOICES)
        return f"{self.name}, Type: {types[self.type]},Interest Rate: {self.interest_rate}"


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
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=2, choices=TYPES_CHOICES, default=PENDING)  #True ==> Accepted   |   False ==> Pending
    loan_fund = models.ForeignKey(LoanFund, on_delete=models.PROTECT, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="applications")

    def get_status(self):
        types = dict(self.TYPES_CHOICES)
        return types[self.status]

    def __str__(self):
        return f"{self.user.get_full_name()}, Loan/Fund Name: {self.loan_fund.name}, Status: {self.get_status()}"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    date = models.DateTimeField()
    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name="payments")

