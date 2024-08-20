# forms.py

from django import forms
from CoreApps.Station.models import Station
from CoreApps.Sensor.models import Sensor

class ReportForm(forms.Form):
    sensor = forms.ModelChoiceField(
        queryset=Sensor.objects.none(),
        label='Sensor'
    )
#agregado el llamado a los sensores para nuevo campo
    #sensor = forms.ModelChoiceField(
    #    queryset=Sensor.objects.none(),
    #    required=False
    #)
#Aqui termina lo agregado

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


    #def __init__(self, user, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    # Filtra las estaciones basadas en el usuario logeado
    #    self.fields['station'].queryset = Station.objects.filter(user_ID=user)
    #    #se agrega nueva funcionalidad para filtrar los sensores asociados
    #    #if 'station' in self.data:
    #    #    try:
    #    #        station_id = int(self.data.get('station'))
    #    #        self.fields['sensor'].queryset = Sensor.objects.filter(stationID=station_id)
    #    #    except (ValueError, TypeError):
    #    #        self.fields['sensor'].queryset = Sensor.objects.none()
    #    #else:
    #    #    self.fields['sensor'].queryset = Sensor.objects.none()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que el campo 'sensor' esté definido antes de asignar el queryset
        if 'sensor' in self.fields:
            user_stations = Station.objects.filter(user_ID=user)
            print(f"Estaciones del usuario: {user_stations}")
            sensors = Sensor.objects.filter(stationID__in=user_stations)
            print(f"Sensores disponibles: {sensors}")
            self.fields['sensor'].queryset = sensors