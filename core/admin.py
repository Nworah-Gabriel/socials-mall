from django.contrib import admin
from  .models import *


class InstagramServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class FacebookServiceServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']

class TiktokServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class YoutubeServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class TelegramServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class TwitterServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class AuidioMackServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service', 'price_per_k']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["type_of", "name", "description", "price"]

class AccountAdmin(admin.ModelAdmin):
    list_display = ["type_of", "category", "file", "is_sold"]

class PurchaseAdmin(admin.ModelAdmin):
    list_display= ["user", "account", "date"]
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "date", "confirmed"]

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order)
admin.site.register(InstagramService, InstagramServiceAdmin)
admin.site.register(FacebookService, FacebookServiceServiceAdmin)
admin.site.register(TiktokService, TiktokServiceAdmin)
admin.site.register(YoutubeService, YoutubeServiceAdmin)
admin.site.register(TelegramService, TelegramServiceAdmin)
admin.site.register(Twitter, TwitterServiceAdmin)
admin.site.register(AudioMack, AuidioMackServiceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(PurchaseHistory)
admin.site.register(DeliveryItem)