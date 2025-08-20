import uuid
from phonenumber_field.modelfields import PhoneNumberField
from authtools.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now

class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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
    balance = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    payment_image = models.ImageField(upload_to='customer/payment/', null=True, blank=True)
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading = models.BooleanField(
        choices=TRADING_CHOICES,
        default=POSITIVE,
    )

    class Meta:
        app_label = 'customer'


class Bet(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    summa = models.IntegerField()
    open_date = models.DateTimeField(db_default=now())
    close_date = models.DateTimeField()
    entry = models.IntegerField()
    profit = models.IntegerField()

    class Meta:
        app_label = 'customer'