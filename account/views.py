import mailbox
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
# Create your views here.

def register(request):
    if request.user.is_authenticated and request.method == "GET":
        return redirect("core:dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("core:dashboard")
        else:
            messages.error(request, form.errors)
    form = SignUpForm()
    return render(request, "signup.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect("core:index")