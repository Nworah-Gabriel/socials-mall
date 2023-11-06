from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
from django.core.mail import EmailMessage


# @shared_task
def check_bal():
    api_url = "https://the-owlet.com/api/v2"

    url = "https://the-owlet.com/api/v2"

    payload = json.dumps({
        "key": settings.OWLET_API_KEY,
        "action": "balance"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = response.json()
    amount = data["amount"]
    if amount <= 20000.00: # Change this to the desired amount
        email = EmailMessage(
                'Owlet Balance Notifier',
                'Please kindly fund your owlet, balance is running low',
                settings.EMAIL_HOST_USER,
                ["sylvaejike@gmail.com"],
        )
        email.send()