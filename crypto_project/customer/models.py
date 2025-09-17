import uuid
from phonenumber_field.modelfields import PhoneNumberField
from authtools.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.user and hasattr(self.user, 'name'):
            return '{name} <{email}>'.format(
                name=self.user.name,
                email=self.user.email,
            )
        else:
            return 'No user'

    class Meta:
        app_label = 'customer'


class Customer(models.Model):
    POSITIVE = True
    NEGATIVE = False

    TRADING_CHOICES = {
        POSITIVE: " + Positive",
        NEGATIVE: " - Negative",
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{5}(-\d{4})?$",
                message="Enter a valid US zip code."
            )
        ], null=True, blank=True
    )
    address = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    job_address = models.CharField(max_length=200, null=True, blank=True)
    job_type = models.CharField(max_length=200, null=True, blank=True)
    balance = models.FloatField(default=0)
    is_verified = models.BooleanField(default=False)
    payment_image = models.ImageField(upload_to='customer/payment/', null=True, blank=True)
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading = models.BooleanField(
        choices=TRADING_CHOICES,
        default=POSITIVE,
    )

    def __str__(self):
        if self.user and hasattr(self.user, 'name'):
            return '{name} <{email}>'.format(
                name=self.user.name,
                email=self.user.email,
            )
        else:
            return 'No user'

    class Meta:
        app_label = 'customer'


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comment to {name}'.format(
            name=self.customer.user.name,
        )

    class Meta:
        app_label = 'customer'


class Bet(models.Model):
    QUOTES_CHOICES = {
        "GBPUSD": "GBP/USD",
        "USDJPY": "USD/JPY",
        "USDCHF": "USD/CHF",
        "AUDUSD": "AUD/USD",
        "EURUSD": "EUR/USD",
    }

    TYPE_CHOICES = {
        "buy": "BUY",
        "sell": "SELL"
    }

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    quotation = models.CharField(max_length=6, choices=QUOTES_CHOICES, null=True, blank=True)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, null=True, blank=True)
    summa = models.FloatField(default=0)
    open_date = models.DateTimeField(default=timezone.now)
    close_date = models.DateTimeField(null=True, blank=True)
    entry = models.FloatField(default=0)
    profit = models.FloatField(default=0)

    class Meta:
        app_label = 'customer'