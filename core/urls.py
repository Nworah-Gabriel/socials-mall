from django.urls import path 
from . import views


app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("faq/", views.faq, name="faq"),
    path("services/", views.services, name="services"),
    path("user/services/", views.userServices, name="userservices"),
    path("user/handles/", views.handles, name="handles"),
    path("user/dashboard/", views.dashboard, name="dashboard"),
    path("user/addfunds/", views.addFunds, name="addfunds"),
    path("user/orders/", views.orders, name="orders"),
    path("user/account/", views.account, name="account"),
    path("user/delivery/", views.delivery, name="delivery"),
    path("user/purchasehistory/", views.purchaseHistory, name="purchasehistory"),
    path("user/flutterwave/payment/preview/<str:ref>/", views.flutterWavePaymentPreviewPage, name="flutterpaymentpreview"),
    path("user/korapay/payment/preview/<str:ref>/", views.korapayPreviewPage, name="korapaypreview"),
    path("user/crypto/payment/preview/", views.cryptoPaymentPreviewPage, name="cryptopaymentpreview"),
    path("user/deposit/flutterwave/success/", views.flutterwaveSuccess, name="flutterwavesuccess"),
    path("user/deposit/success/", views.cryptosuccess, name="cryptosuccess"),
    path("user/deposit/cancel/", views.cancel, name="cancel"),
    path("user/handles/purchase/<int:id>/", views.purchase, name="purchase"),
    path("user/handles/facebooks/", views.facebooks, name="facebooks"),
    path("user/handles/facebookdating/", views.facebookdating, name="facebookdating"),
    path("user/handles/facebookads/", views.facebookads, name="facebookads"),
    path("user/handles/twitters/", views.twitters, name="twitters"),
    path("user/handles/newinstagrams/", views.newinstagrams, name="newinstagrams"),
    path("user/handles/oldinstagrams/", views.oldinstagrams, name="oldinstagrams"),
    path("user/handles/fanpages/", views.fanpages, name="fanpages"),
    path("user/handles/google-voice/", views.googleVoices, name="googlevoices"),
    path("user/handles/linkedin/", views.linkedins, name="linkedins"),
    path("user/handles/netflix/", views.netflix, name="netflix"),
    path("user/handles/tiktok/", views.titoks, name="tiktoks"),
    path("user/handles/vpn/", views.vpns, name="vpns"),
    path("user/handles/gmail/", views.gmail, name="gmail"),
    path("user/handles/snapchat/", views.snapchat, name="snapchat"),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path("flutterwave/webhook/", views.flutterwaveWebhook, name="flutterwavewebhook"),
    path("korapay/webhook/", views.korapayWebhook, name="korapaywavewebhook"),
]