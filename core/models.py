from django.db import models
from account.models import User
from django.utils import timezone
import uuid 


TYPE_ = (
    ("Facebook", "Facebook"),
    ("Facebook Dating", "Facebook Dating"),
    ("Google Voice", "Google Voice"),
    ("New Instagram", " New Instagram"),
    ("Old Instagram", " Old Instagram"),
    ("Twitter", "Twitter"),
    ("VPN", "VPN"),
    ("Facebook ADS", "Facebook ADS"),
    ("Netflix", "Netflix"),
    ("Tiktok", "Tiktok"),
    ("Gmail", "Gmail"),
    ("Snapchat", "Snapchat"),
    ("OLD FANPAGE", "OLD FANPAGE"),
    ("Linkedin", "Linkedin"),
)


# Create your models here.
class DeliveryItem(models.Model):
    item = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(default=0)
    
    def __str__(self):
        return self.item
        
        
class Payment(models.Model):
    transaction_ref = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0)
    method = models.CharField(max_length=100, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.amount)


class Order(models.Model):
    orderid = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=150, null=True, blank=True)
    amount = models.FloatField()
    quantity = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=100000, null=True, blank=True)
    status = models.CharField(
        max_length=50, default="in progress", null=True, blank=True
    )
    refil_status = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.user)


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account = models.CharField(max_length=150, null=True, blank=True)
    price = models.FloatField(default=0)
    file = models.FileField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = "Purchase History"
        verbose_name_plural = "Purchase Histories"


class InstagramService(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class TiktokService(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.service


class YoutubeService(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class TelegramService(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class FacebookService(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class Twitter(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class AudioMack(models.Model):
    service = models.CharField(
        max_length=150, default="", null=True, blank=True, unique=True
    )
    minimum = models.PositiveIntegerField()
    maximum = models.PositiveIntegerField()
    price_per_k = models.FloatField(default=0)
    service_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.service


class Handle(models.Model):
    type_of = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    price = models.FloatField()
    file = models.FileField(default=timezone.now)
    is_sold = models.BooleanField(default=False)
    link = models.CharField(max_length=1000, null=True, blank=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description


class Category(models.Model):
    type_of = models.CharField(
        choices=TYPE_,
        default=TYPE_[0],
        max_length=150,
    )
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=150, default="", null=True, blank=False)
    price = models.FloatField(default=0)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Account(models.Model):
    type_of = models.CharField(choices=TYPE_, default=TYPE_[0], max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    # description = models.CharField(max_length=150, default="", null=True, blank=False)
    is_sold = models.BooleanField(default=False)
    file = models.FileField(default=timezone.now, upload_to="logs")
    # price = models.FloatField()

    def save(self, *args, **kwargs):
        accounts = Account.objects.filter(category=self.category, is_sold=False).count()
        try:
            category = Category.objects.get(id=self.category.id)
            category.count = accounts
            category.save()
            super().save(*args, **kwargs)
        except Category.DoesNotExist:
            pass

    def __str__(self):
        return self.type_of


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Payment History"
        verbose_name_plural = "Payment Histories"

    def __str__(self):
        return str(self.user)




# import requests
# from core.models import *

# def update_prices_from_api():
#     # Define the API endpoint
#     api_endpoint = "https://the-owlet.com/api/v2"  # Replace with your API endpoint

#     try:
#         # Fetch the services from your Django model
#         services = AudioMack.objects.all()

#         # Make the POST request to the API
#         response = requests.post(
#             api_endpoint,
#             json={"key": "1eb48bcd241cfc669dba493c19eae46c", "action": "services"},
#         )
#         api_data = response.json()
#         print(api_data)
    

#         # Process the API response
#         for api_service in api_data:
#             api_service_id = api_service.get("service")
#             api_service_price = api_service.get("rate")

#             if api_service_id is not None and api_service_price is not None:
#                 try:
#                     # Find the corresponding service in your Django model
#                     service = services.get(service_id=api_service_id)

#                     # Compare with the existing price and update if needed
#                     if service.price_per_k != api_service_price:
#                         service.price_per_k = float(api_service_price) + 500.0
#                         service.save()
#                         print(f"Updated price for service ID {service.id}")
#                 except AudioMack.DoesNotExist:
#                     print(f"Service ID {api_service_id} not found in Django model")
#                     # Delete the service from the database since it doesn't exist in the API response

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data from API: {e}")

