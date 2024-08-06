from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=20)
    email = forms.CharField(label='Email', max_length=30)
    telefono = forms.CharField(label='Teléfono', max_length=30)
    contenido = forms.CharField(label='Contenido', max_length=400, widget=forms.Textarea)
