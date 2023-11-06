from django.db.models.signals import post_save
from .models import Payment
import uuid
from django.dispatch import receiver


"""
auto increment the film comment count field after each comment is saved
"""
@receiver(post_save, sender=Payment)
def generate_transaction_ref(sender, instance, created, **kwargs):
    if created and not instance.transaction_ref:
        # Generate a unique transaction_ref using UUID
        instance.transaction_ref = str(uuid.uuid4())
        instance.save()
            