import uuid
from phonenumber_field.modelfields import PhoneNumberField
from authtools.models import User
from django.db import models
from django.core.validators import RegexValidator



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone_number = PhoneNumberField(blank=False)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{5}(-\d{4})?$",
                message="Enter a valid US zip code."
            )
        ]
    )
    address = models.CharField(max_length=200)
    birth_date = models.DateField()
    job_address = models.CharField(max_length=200)
    job_type = models.CharField(max_length=200)
    balance = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    payment_image = models.ImageField(upload_to='customer/payment/')
    iban = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)