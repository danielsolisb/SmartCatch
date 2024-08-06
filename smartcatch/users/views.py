from django.shortcuts import render,  redirect
from .forms import RegisterForm

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import auth
# Agregada librerias para uso de registro y verificación de cuentas
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register.html", {"form": form})



