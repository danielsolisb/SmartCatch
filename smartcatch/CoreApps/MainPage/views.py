
from typing import Any
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView, DetailView, View, FormView
from .forms import FormularioContacto

def page_not_found404(request, exception):
    return render(request, '404.html')

class main(TemplateView):
    template_name = 'index.html'

class about(TemplateView):
    template_name = 'about.html'

#class contact(TemplateView):
#    template_name = 'contact.html'
class acuicultura(TemplateView):
    template_name = 'acuicultura.html'
class industrial(TemplateView):
    template_name = 'industrial.html'
class agroIoT(TemplateView):
    template_name = 'agricola.html'

class avicolaIoT(TemplateView):
    template_name = 'avicola.html'


def contact(request):

    formulario_contacto=FormularioContacto()

    if request.method=="POST":
        formulario_contacto=FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre=request.POST.get("nombre")
            email=request.POST.get("email")
            telefono=request.POST.get("telefono")
            contenido=request.POST.get("contenido")
            print(nombre)
            print("---------------")
            email=EmailMessage("Mensaje de app Techdevsa",
            "El usuario con nombre {} con la dirección {} y el telefono {} escribe lo siguiente:\n\n {}".format(nombre, email, telefono, contenido), 
            '',
            ["techdevsa01@gmail.com"], 
            reply_to=[email])
            print(email)
            try:
                email.send()

                return redirect("mainpage")
            except:
                return redirect("contacto")

    return render(request, "contact.html", {'miFormulario':formulario_contacto})

def demoRequest(request):

    formulario_contacto=FormularioContacto()

    if request.method=="POST":
        formulario_contacto=FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre=request.POST.get("nombre")
            email=request.POST.get("email")
            telefono=request.POST.get("telefono")
            contenido=request.POST.get("contenido")
            print(nombre)
            print("---------------")
            email=EmailMessage("Mensaje de app Techdevsa",
            "El usuario con nombre {} con la dirección {} y el telefono {} solicita un demo request y escribe lo siguiente:\n\n {}".format(nombre, email, telefono, contenido), 
            '',
            ["techdevsa01@gmail.com"], 
            reply_to=[email])
            print(email)
            try:
                email.send()

                return redirect("/Portal/login")
            except:
                return redirect("/Portal/login")

    return render(request, "DemoRequest.html", {'miFormulario':formulario_contacto})