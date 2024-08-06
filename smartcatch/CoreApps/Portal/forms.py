# forms.py

from django import forms
from CoreApps.Station.models import Station

#class ReportForm(forms.Form):
#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop('user', None)  # Obtener el usuario de los argumentos (si se proporciona)
#        super(ReportForm, self).__init__(*args, **kwargs)
#        print(user)
#        if user:
#            self.fields['station'].queryset = Station.objects.filter(user_ID=user)
#            
#
#
#    station = forms.ModelChoiceField(
#        queryset=Station.objects.none(),  # Establecer una queryset inicial vacía
#        label='Selecciona una estación'
#    )
#    start_date = forms.DateField(label='Fecha de inicio')
#    end_date = forms.DateField(label='Fecha de fin')


class ReportForm(forms.Form):
    station = forms.ModelChoiceField(
        queryset=Station.objects.none(),
        #label='Estación'
    )

    start_date = forms.DateTimeField(
        #label='Fecha de inicio',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=["%Y-%m-%dT%H:%M"]
    )
    end_date = forms.DateTimeField(
        #label='Fecha de fin',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=["%Y-%m-%dT%H:%M"]
    )

    #def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user', None)  # Obtiene el usuario logeado si se pasa como argumento
    #    super().__init__(*args, **kwargs)
    #    if user:
    #        # Filtra las estaciones basadas en el usuario logeado
    #        self.fields['station'].queryset = Station.objects.filter(user=user)


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las estaciones basadas en el usuario logeado
        self.fields['station'].queryset = Station.objects.filter(user_ID=user)