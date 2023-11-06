from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from account.models import User
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from .utils import *
import mimetypes
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from email.mime.application import MIMEApplication
from email import encoders
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import random
import string
from coinbase_commerce.client import Client
from decimal import Decimal
# Create your views here.

flutterWavePublicKey = settings.FLUTTER_API_PUBLIC_KEY
korapayPublicKey = settings.KORAPAY_API_PUBLIC_KEY

def index(request):
    if request.user.is_authenticated and request.method == "GET":
        return redirect("core:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("core:dashboard")
                
            else:
                messages.error(request, "User does not exit")
        else:
            messages.error(request, form.errors)
            return redirect("core:index")

    form = AuthenticationForm()
    return render(request, "index.html", context={"form": form})


def services(request):
    return render(request, "services.html")

def faq(request):
    return render(request, "faq.html")

@login_required(login_url="core:index")
def dashboard(request):
    orders = Order.objects.all().count()
    facebookService = FacebookService.objects.all()
    instagramService = InstagramService.objects.all()
    telegramService = TelegramService.objects.all() 
    youtubeService = YoutubeService.objects.all()
    tiktokService = TiktokService.objects.all()
    twitterService = Twitter.objects.all()
    audiomackService = AudioMack.objects.all()


    userid = request.user.id
    user = User.objects.get(id=userid)
    
    if request.method == "POST":
        
        user = User.objects.get(id=request.user.id)
        userBalance = user.balance
        bill = request.POST["price"]
        serviceId = request.POST["serviceid"]
        service = request.POST["servicedescri"]
        link = request.POST["link"]
        quantity = request.POST["quantity"]
        
        models = [FacebookService, InstagramService, TelegramService, YoutubeService, TiktokService, Twitter, AudioMack]

        
        for model_class in models:
            try:
                # Query the current model for the service ID
                result = model_class.objects.get(service_id=serviceId)
                if int(quantity) < result.minimum:
                    messages.warning(request, "Quantity provided is lesser than the minimum specified")
                    return redirect("core:dashboard")
                elif int(quantity) > result.maximum:
                    messages.warning(request, "Quantity provided is greaten than the maximum specified")
            except model_class.DoesNotExist:
                pass
    
        chkBal = checkBalance(bill, userBalance)
        if not chkBal:
            messages.warning(request, "Insufficient funds")
            messages.info(request, "Kinldy fund your account")
            return redirect("core:addfunds")
        else:
            debitBalance(request.user.id, bill)
            url = "	https://the-owlet.com/api/v2"

            try:
                payload = json.dumps({
                    "key": settings.OWLET_API_KEY,
                    "action": "add",
                    "service": serviceId,
                    "link": link,
                    "quantity": quantity
                })
                
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                responseData = response.json()
                orderId = responseData["order"]

                Order.objects.create(
                    orderid = orderId,
                    user = user,
                    service = service,
                    amount = int(bill[1:-3]),
                    link = link,
                    quantity=quantity
                )
                messages.success(request, 
                    f"ID: {orderId}\nService Name: {service}\nLink: {link}\nQuantity: {quantity}"
                )
                return redirect("core:dashboard")
            except Exception as e:
                messages.error(request, e)
                return redirect("core:dashboard")
    data = {
        "balance": user.balance,
        "facebookService": facebookService,
        "instagramService": instagramService,
        "telegramService": telegramService,
        "youtubeService": youtubeService,
        "tiktokService": tiktokService,
        "twitterService": twitterService,
        "audiomackService": audiomackService,
        "orders": orders,
        "page": "dashboard"
    }
    return render(request, "dashboard.html", context=data)


@login_required(login_url="core:index")
def addFunds(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    paymenthistory = PaymentHistory.objects.filter(user=user)

    # try:
    #     Payment.objects.filter(user=user).all().delete()
    # except Payment.DoesNotExist:
    #     pass

    if request.method == "POST" and request.POST["method"] == "flutterwave":
        amount = float(request.POST['amount'])
        method = request.POST["method"]
        payment = Payment.objects.create(user=user, amount=amount, method=method)
        url = reverse('core:flutterpaymentpreview', kwargs={'ref': payment.transaction_ref})
        return redirect(url)
    elif request.method == "POST" and request.POST["method"] == "korapay":
        amount = float(request.POST['amount'])
        method = request.POST["method"]
        payment = Payment.objects.create(user=user, amount=amount, method=method)
        url = reverse('core:korapaypreview', kwargs={'ref': payment.transaction_ref})
        return redirect(url)
    elif request.method == "POST" and request.POST["method"] == "crypto":
        amount = float(request.POST['amount'])
        method = request.POST["method"]
        Payment.objects.create(user=user, amount=amount, method=method)
        return redirect("core:cryptopaymentpreview")

    data = {
        "paymenthistory": paymenthistory,
        "page": "addfunds",
        "balance": user.balance,
    }

    return render(request, "addfunds.html", context=data)


@login_required(login_url="core:index")
def flutterWavePaymentPreviewPage(request, ref):
    user = User.objects.get(id=request.user.id)
    try:
        depositprev = Payment.objects.get(user=user, transaction_ref=ref)
    except Payment.DoesNotExist:
        return redirect("core:addfunds")
    data = {
        "flutterwavePublickey": flutterWavePublicKey,
        "payment": depositprev,
    }
    return render(request, "flutterwavepaymentpreview.html", context=data)


@login_required(login_url="core:index")
def korapayPreviewPage(request, ref):
    user = User.objects.get(id=request.user.id)
    try:
        depositprev = Payment.objects.get(user=user, transaction_ref=ref)
    except Payment.DoesNotExist:
        return redirect("core:addfunds")
    data = {
        "korapayPublickey": korapayPublicKey,
        "payment": depositprev,
    }
    return render(request, "korapaypaymentpreview.html", context=data)


@login_required(login_url="core:index")
def cryptoPaymentPreviewPage(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    payment = Payment.objects.get(user=user)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = "https://socialsmall.net"
    product = {
        'name': 'Socials Deposit',
        'description': 'funding of socials mall account',
        'local_price': {
            'amount': f"{payment.amount}",
            'currency': 'NGN'
        },  
        'pricing_type': 'fixed_price',
        'redirect_url': domain_url + '/user/deposit/success/',
        'cancel_url': domain_url + '/user/deposit/cancel/',
        'metadata': {
            'customer_id': request.user.id if request.user.is_authenticated else None,
            'customer_username': request.user.username if request.user.is_authenticated else None,
        },
    }
    charge = client.charge.create(**product)

    data = {
        "preview": payment,
        "charge": charge
    }

    
    return render(request, "cryptopaymentpreview.html", context=data)

@login_required(login_url="core:index")
def account(request):
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Your password has been updated")
            return redirect(reverse("core:dashboard"))

    return render(request, "account.html", {"password_form": password_form} )

@login_required(login_url="account:index")
def cancel(request):
    messages.warning(request, "Deposit failed")
    return redirect("core:dashboard")
    
@login_required(login_url="core:index")
def cryptosuccess(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    prev = Payment.objects.get(user=user)

    user.balance += prev.amount
    user.save()
    PaymentHistory.objects.create(
        user=user,
        amount=prev.amount,
        method = "crypto"
    )
    messages.success(request, "deposit successful")
    return redirect("core:dashboard")


@login_required(login_url="core:index")
def userServices(request):
    handles = Handle.objects.filter(is_sold=False)

    data = {
        "handles": handles
    }
    return render(request, "userservices.html", context=data)


@login_required(login_url="core:index")
def flutterwaveSuccess(request):
    messages.success(request, "Deposit successful")
    return redirect("core:dashboard")
    

@login_required(login_url="core:index")
def orders(request):
    userid = request.user.id
    user = User.objects.get(id=userid)
    orders = Order.objects.filter(user=user)


    # check order status
    url = "https://the-owlet.com/api/v2"
    if orders.count() > 0:
        for i in orders:

            payload = json.dumps({
                "key": settings.OWLET_API_KEY,
                "action": "status",
                "order": i.orderid
            })
            
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            responseData = response.json()
           
            status = responseData["status"]
            i.status = status 
            i.save()
        
    data = {
        "orders": orders,
        "page": "orders",
        "balance": user.balance,
    }
    return render(request, "orders.html", context=data)


@login_required(login_url="core:index")
def handles(request):
    user = User.objects.get(id=request.user.id)
    data = {
        "page": "accounts",
        "balance": user.balance
    }
    return render(request, "handles.html", context=data)


@login_required(login_url="core:index")
def purchaseHistory(request):
    user = User.objects.get(id=request.user.id)
    history = PurchaseHistory.objects.filter(user=request.user).order_by("-date")
    data = {
        "page": "purchase history",
        "histories": history,
        "balance": user.balance,
    }
    return render(request, "purchase_history.html", context=data)

    
@login_required(login_url="core:index")
def purchase(request, id):
    userBalance = request.user.balance
    user = User.objects.get(id=request.user.id)
    category = Category.objects.get(id=id)
    accounts = Account.objects.filter(type_of = category.type_of, category=category.id, is_sold = False).count()

    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        accounts_ = Account.objects.filter(type_of = category.type_of, category=category.id, is_sold = False)[:quantity]
        
        if accounts >=  quantity:
            try:
                bill = category.price * quantity

                if int(bill) > int(userBalance):
                    messages.warning(request, "Insufficient funds")
                    messages.info(request, "Kinldy fund your account")
                    return redirect("core:addfunds")
                else:
                    user.balance -= Decimal(str(bill))
                    user.save()
                    
                    
                    for i in accounts_:
                        
                        PurchaseHistory.objects.create(
                            user = user,
                            account = category.name,
                            price = category.price,
                            file = i.file,
                        )
                        
                        i.to = request.user
                        i.is_sold = True
                        i.save()
                        messages.success(request, "kindly check your user email for account details")
                    return redirect("core:purchasehistory")
            except Exception as e:
                
                messages.error(request, e)
                return redirect("core:dashboard")
        else:
            messages.warning(request, "Insufficient funds")
            messages.info(request, "Kindly fund your account")
            return redirect("core:dashboard")
    
    data = {
        "category": category
    }
    return render(request, "purchase.html", context=data)


@login_required(login_url="core:index")
def facebooks(request):
    categories = Category.objects.filter(type_of = "Facebook")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Facebook", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/facebooks.html", context=data)

@login_required(login_url="core:index")
def facebookdating(request):
    categories = Category.objects.filter(type_of = "Facebook Dating")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Facebook Dating", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/facebookdating.html", context=data)
    
@login_required(login_url="core:index")
def facebookads(request):
    categories = Category.objects.filter(type_of="Facebook ADS")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of="Facebook ADS", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/facebookads.html", context=data)

@login_required(login_url="core:index")
def newinstagrams(request):
    categories = Category.objects.filter(type_of = "New Instagram")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "New Instagram", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
        "accounts": accounts
    }
    return render(request, "handles/instagrams.html", context=data)
    
@login_required(login_url="core:index")
def oldinstagrams(request):
    categories = Category.objects.filter(type_of = "Old Instagram")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Old Instagram", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
        "accounts": accounts
    }
    return render(request, "handles/instagrams.html", context=data)

@login_required(login_url="core:index")
def twitters(request):
    categories = Category.objects.filter(type_of = "Twitter")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Twitter", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/twitters.html", context=data)

@login_required(login_url="core:index")
def fanpages(request):
    categories = Category.objects.filter(type_of = "OLD FANPAGE")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "OLD FANPAGE", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/old-fanpage.html", context=data)

@login_required(login_url="core:index")
def googleVoices(request):
    categories = Category.objects.filter(type_of = "Google Voice")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Google Voice", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/google-voice.html", context=data)

@login_required(login_url="core:index")
def linkedins(request):
    categories = Category.objects.filter(type_of = "Linkedin")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Linkedin", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/linkedin.html", context=data)

@login_required(login_url="core:index")
def netflix(request):
    categories = Category.objects.filter(type_of = "Netflix")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Netflix", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/netflix.html", context=data)

@login_required(login_url="core:index")
def titoks(request):
    categories = Category.objects.filter(type_of = "Tiktok")
    if categories.count() < 1:
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Tiktok", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/tiktok.html", context=data)

@login_required(login_url="core:index")
def vpns(request):
    categories = Category.objects.filter(type_of = "VPN")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "VPN", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/vpn.html", context=data)

@login_required(login_url="core:index")
def gmail(request):
    categories = Category.objects.filter(type_of = "Gmail")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Gmail", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/gmail.html", context=data)


@login_required(login_url="core:index")
def snapchat(request):
    categories = Category.objects.filter(type_of = "Snapchat")
    if categories.count() < 1:
        messages.info(request, "None available at the moment")
        return redirect("core:handles")
    for i in categories:
        accounts = Account.objects.filter(type_of = "Snapchat", category=i.id, is_sold = False).count()
        i.count = accounts
        i.save()

    data = {
        "categories": categories,
    }
    return render(request, "handles/snapchat.html", context=data)
    

@login_required(login_url="core:index")   
def delivery(request):
    user = User.objects.get(id=request.user.id)
    data = {
            "items": DeliveryItem.objects.all(),
            "page": "delivery",
            "balance": user.balance,
        }
    if request.method == "POST":
        service = DeliveryItem.objects.get(item=request.POST["service"])
        price = service.amount
        
        if float(price) > request.user.balance:
            messages.error(request, "Insufficient funds, Kindly fund your account")
            return redirect("core:addfunds")
        else:
            user = User.objects.get(id=request.user.id)
            user.balance -= Decimal(str(price))
            user.save()
            messages.success(request, "Order Submitted, standby for response")
            msgdata = f'The user with username:{request.user.username} chose the {service} service. Price: {price} Recipent Contact details: {request.POST["link"]}. Kindly contact this user and take the order as soon as you can.',
                
            try:
                import requests
                import json
            
                # API endpoint URL
                url = 'https://api.emailjs.com/api/v1.0/email/send'  # Replace this with the actual API endpoint URL
                
                # Sample parameters in a Python dictionary
                params = {
                    'service_id': 'service_ln7m2eo',
                    'template_id': 'template_kmmtb7l',
                    'user_id': 'WiOGNs564kdOqYiZx',    
                    "template_params": {
                        'message': json.dumps(msgdata),
                        'from_name': 'Socials Mall'
                    }
                }
            
                # Convert the parameters dictionary to a JSON string
                json_params = json.dumps(params)
            
                # Headers with 'Content-Type: application/json'
                headers = {'Content-Type': 'application/json', 'origin': 'https://socialsmall.net'}
            
                # Make the POST request
                response = requests.post(url, data=json_params, headers=headers)
            
                # Check if the request was successful (status code 200-299 usually indicates success)
                if response.status_code >= 200 and response.status_code < 300:
                    pass
                    #print("Request successful!")
                    #print("Response data:")
                    # #print(response.json())  # If the response is in JSON format
                else:
                    pass
                    #print(f"Request failed with status code: {response.status_code}")
                    #print("Response data:")
                    # #print(response.text)
            
                #print("email sent")
            except Exception as e:
                return redirect("core:dashboard")
                
            return redirect("core:dashboard")
            
        
    return render(request, "delivery.html", context=data)


def download_file(request, pk):
    my_model_instance = PurchaseHistory.objects.get(pk=pk)
    file = my_model_instance.file
    response = HttpResponse(file)
    response['Content-Disposition'] = 'attachment; filename=%s' % file.name
    return response


@csrf_exempt
def flutterwaveWebhook(request):
    if request.method == "POST":
        secret_hash =  settings.FLUTTERWAVE_WEBHOOK_HASH
        signature = request.headers.get("verif-hash")
        if signature == None or (signature != secret_hash):
            # This request isn't from Flutterwave; discard
            return HttpResponse(status=401)

        # Retrieve the raw JSON data from the request
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Process the webhook data and confirm the payment
        # You can implement your payment confirmation logic here
        # Make sure to verify the authenticity of the webhook data
        # Process the webhook data and confirm the payment
        event_type = payload.get("event")
        
        if event_type == "charge.completed":
            transaction_ref = payload["data"]["tx_ref"]
            # Query your database to find the user associated with this transaction
            # try:
            payment = Payment.objects.get(transaction_ref=transaction_ref)
            if payment.confirmed == True:
                return JsonResponse({"status": "Webhook received"}, status=200)
                
            else:   
                payment.confirmed = True
                payment.save()
                
                user = payment.user
                # Update the user's balance
                payloadamount = payload["data"]["amount"]
                user.balance += Decimal(str(payloadamount))
                user.save()
                return JsonResponse({"status": "Webhook received"}, status=200)
            # except Payment.DoesNotExist:
            #     return JsonResponse({"error": "Payment not found"}, status=404)

    return HttpResponse(status=405)


@csrf_exempt
def korapayWebhook(request):
    if request.method == "POST":
        secret_hash =  settings.WEBHOOK_HASH
        signature = request.headers.get("x-korapay-signature")
        if signature == None or (signature != secret_hash):
            # This request isn't from Flutterwave; discard
            return HttpResponse(status=401)

        # Retrieve the raw JSON data from the request
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Process the webhook data and confirm the payment
        # You can implement your payment confirmation logic here
        # Make sure to verify the authenticity of the webhook data
        # Process the webhook data and confirm the payment
        event_type = payload.get("event")
        
        if event_type == "charge.success":  
            transaction_ref = payload["data"]["payment_reference"]
            # Query your database to find the user associated with this transaction
            # try:
            payment = Payment.objects.get(transaction_ref=transaction_ref)
            if payment.confirmed == True:
                return JsonResponse({"status": "Webhook received"}, status=200)
                
            else:   
                payment.confirmed = True
                payment.save()
                
                user = payment.user
                # Update the user's balance
                payloadamount = payload["data"]["amount"]
                user.balance += Decimal(str(payloadamount))
                user.save()
                return JsonResponse({"status": "Webhook received"}, status=200)
            # except Payment.DoesNotExist:
            #     return JsonResponse({"error": "Payment not found"}, status=404)

    return HttpResponse(status=405)
    