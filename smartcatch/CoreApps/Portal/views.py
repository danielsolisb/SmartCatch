from typing import Any
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, TemplateView, DetailView, View, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from .forms import ReportForm
#Modelos y formularios del user
from users.models import User
from users.forms import UserUpdateForm



from CoreApps.Station.models import Station
from CoreApps.Sensor.models import Sensor, Alarm, Actuator
from CoreApps.Measurement.models import Measurements, Measurements_actuators

from django.db.models import Max
from collections import defaultdict

def page_not_found404(request, exception):
    return render(request, '404.html')

class Dashboard(TemplateView):
    template_name = 'Dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        # Obtenemos la categoría del usuario logeado
        user = self.request.user
        user_category = user.categorie
        # Determinamos la plantilla según la categoría
        if user_category == 'industrial':
            return ["DashIndu.html"]
        elif user_category == 'agricola':
            return ["DashAgro.html"]
        elif user_category == 'avicola':
            return ["DashAvi.html"]
        else:
            return [self.template_name]  # Usar la plantilla por defecto si la categoría no coincide
        
    def get_context_data(self, **kwargs):
        user = self.request.user
        user_category = user.categorie
        context = super().get_context_data(**kwargs)
        #Agregamos información al context
        user_stations = Station.objects.filter(user_ID=self.request.user)
        # filtradas las alarmas relacionadas al usuario logeado
        user_sensor_alarms = Alarm.objects.filter(sensor__stationID__user_ID=user)
        #filtramos el tipo de alarmas
        user_alarms = user_sensor_alarms.filter(alarm_type='alarm')
        #user_warning = user_sensor_alarms.filter(alarm_type='warning').count()
        user_warning = user_sensor_alarms.filter(alarm_type='warning')
        context['user_name'] = user.username
        context['title'] = "Dashboard"
        context['user_stations']= user_stations
        context['stations_num']= len(user_stations)
        context['user_alarms'] = user_alarms
        context['user_warnings'] = user_warning
        if user_category == 'industrial':
            #timestamps = [str(alarm.timestamp) for alarm in user_alarms]
            timestamps = [alarm.timestamp.strftime("%Y-%m-%d %H:%M:%S") for alarm in user_alarms]
            values = [alarm.value for alarm in user_alarms]
            timestampsw = [warning.timestamp.strftime("%Y-%m-%d %H:%M:%S") for warning in user_warning]
            valuesw = [warning.value for warning in user_warning]
            context['timestamps'] = timestamps
            context['values'] = values
            context['timestampsw'] = timestampsw
            context['valuesw'] = valuesw
            return context
        elif user_category == 'agricola':            
            #stations = Station.objects.all()
            sensor_data = {}
            for station in user_stations:
                sensors = Sensor.objects.filter(stationID=station)
                sensor_data[station.name] = sensors
            context['sensor_data'] = sensor_data
            context['station']= user_stations
            return context
            # Puedes agregar más datos de contexto si es necesario

class SensorListView(DetailView):
    model = Station
    template_name = 'sensor_list5.html'
    context_object_name = 'station'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_template_names(self):
        # Obtenemos la categoría del usuario logeado
        user = self.request.user
        user_category = user.categorie
        # Determinamos la plantilla según la categoría
        if user_category == 'industrial':
            return ["sensor_list5_indu_7.html"]
        elif user_category == 'agricola':
            return ["sensor_list5_agro_4.html"]
        elif user_category == 'avicola':
            return ["DashAvi.html"]
        else:
            return [self.template_name]  # Usar la plantilla por defecto si la categoría no coincide

    def get_context_data(self, **kwargs):    
        user = self.request.user
        user_category = user.categorie
        if user_category == 'industrial':
            context = super().get_context_data(**kwargs)
            user = self.request.user
            context['user_name'] = user.username
            context['user_stations'] = Station.objects.filter(user_ID=self.request.user)
            context['station_sensors'] = Sensor.objects.filter(stationID=self.object)
            #actuators
            context['station_actuator'] = Actuator.objects.filter(stationID =self.object )
            context['actuators_names'] = [(f"/{self.object.name}/{actuators.name}/", actuators.name) for actuators in context['station_actuator']]
            # Obtén los nombres de los sensores y pásalos al contexto
            sensor_names = [f"/{self.object.name}/{sensor.sensorName}/" for sensor in context['station_sensors']]
            sensorname = [f"{sensor.sensorName}" for sensor in context['station_sensors']]
            last_measurements = []
            for actuator in context['station_actuator']:
                last_measurement = Measurements_actuators.objects.filter(actuatorsID=actuator).aggregate(Max('timestamp'))
                if last_measurement['timestamp__max']:
                    last_value = Measurements_actuators.objects.get(actuatorsID=actuator, timestamp=last_measurement['timestamp__max']).value
                    if isinstance(last_value, float):
                        last_value = int(last_value)
                else:
                    last_value = None
                last_measurements.append((f"/{self.object.name}/{actuator.name}/",actuator.name, last_value))
            context['last_measurements'] = last_measurements
            context['sensor_names'] = [(f"/{self.object.name}/{sensor.sensorName}/", sensor.sensorName) for sensor in context['station_sensors'] if not sensor.sensorName.startswith("F")]
            context['title'] = self.object.name
            context['subTitle']= "Active Sensors"
            context['sensors_with_f'] = [f"/{self.object.name}/{sensor.sensorName}/" for sensor in context['station_sensors'] if sensor.sensorName.startswith("F")]
            return context
        elif user_category == 'agricola':
            context = super().get_context_data(**kwargs)
            user = self.request.user
            context['user_name'] = user.username
            context['user_stations'] = Station.objects.filter(user_ID=self.request.user)
            context['station_sensors'] = Sensor.objects.filter(stationID=self.object)
            #actuators
            context['station_actuator'] = Actuator.objects.filter(stationID =self.object )
            context['actuators_names'] = [(f"/{self.object.name}/{actuators.name}/", actuators.name) for actuators in context['station_actuator']]
            last_measurements = []
            for actuator in context['station_actuator']:
                last_measurement = Measurements_actuators.objects.filter(actuatorsID=actuator).aggregate(Max('timestamp'))
                if last_measurement['timestamp__max']:
                    last_value = Measurements_actuators.objects.get(actuatorsID=actuator, timestamp=last_measurement['timestamp__max']).value
                    if isinstance(last_value, float):
                        last_value = int(last_value)
                else:
                    last_value = None
                last_measurements.append((f"/{self.object.name}/{actuator.name}/",actuator.name, last_value))
            context['last_measurements'] = last_measurements
            #sensor_names = [f"/{self.object.name}/{sensor.sensorName}/" for sensor in context['station_sensors']]
            #sensorname = [f"{sensor.sensorName}" for sensor in context['station_sensors']]
            context['sensor_names'] = [(f"/{self.object.name}/{sensor.sensorName}/", sensor.sensorName) for sensor in context['station_sensors']]
            context['title'] = self.object.name
            context['subTitle']= "Active Sensors"
            return context

#
#class ReportView(FormView):
#    template_name = 'reports5_charts.html'
#    form_class = ReportForm
#    success_url = '/report/'
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['user'] = self.request.user  # Pasa el usuario logeado al formulario
#        return kwargs
#
#    def form_valid(self, form):
#        station_id = form.cleaned_data['station'].id
#        start_date = form.cleaned_data['start_date']
#        end_date = form.cleaned_data['end_date']
#        print (station_id)
#        print(start_date)
#        # Obtener los sensores asociados a la estación seleccionada
#        sensors = Sensor.objects.filter(stationID=station_id)
#        # Crear un diccionario para almacenar las mediciones por sensor
#        measurements_by_sensor = {}
#        # Obtener las mediciones relacionadas con esos sensores y el rango de fechas
#        for sensor in sensors:
#            measurements = Measurements.objects.filter(
#                sensorID=sensor,
#                timestamp__gte=start_date,
#                timestamp__lte=end_date
#            )
#            # Almacena las mediciones en el diccionario usando el sensor como clave
#            measurements_by_sensor[sensor] = measurements
#        # Puedes pasar 'measurements_by_sensor' a tu plantilla y usar Datatables para mostrar los datos
#        return self.render_to_response(self.get_context_data(form=form, measurements_by_sensor=measurements_by_sensor))
#    
#    def get_context_data(self, **kwargs):      
#        context = super().get_context_data(**kwargs)
#        #for i in measurements:
#        #    print(i.sensorID.sensorName)
#        context['user_stations'] = Station.objects.filter(user_ID=self.request.user)
#        context['subTitle']= "Reports"    
#        user = self.request.user
#        context['user_name'] = user.username
#        return context


class ReportView(FormView):
    template_name = 'reports5_charts.html'
    form_class = ReportForm
    success_url = '/report/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasa el usuario logeado al formulario
        return kwargs

    def form_valid(self, form):
        sensor = form.cleaned_data['sensor']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Obtener las mediciones relacionadas con el sensor seleccionado y el rango de fechas
        measurements = Measurements.objects.filter(
            sensorID=sensor,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        )

        # Agrupar las mediciones por sensor
        measurements_by_sensor = {sensor: measurements}

        # Pasar 'measurements_by_sensor' a la plantilla
        return self.render_to_response(self.get_context_data(form=form, measurements_by_sensor=measurements_by_sensor))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_stations'] = Station.objects.filter(user_ID=self.request.user)
        context['subTitle'] = "Reports"
        context['user_name'] = self.request.user.username
        if 'measurements_by_sensor' in kwargs:
            context['measurements_by_sensor'] = kwargs['measurements_by_sensor']
        return context


#class ReportView(FormView):
#    template_name = 'reports5_charts.html'
#    form_class = ReportForm
#    success_url = '/report/'
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['user'] = self.request.user  # Pasa el usuario logeado al formulario
#        return kwargs
#
#    def form_valid(self, form):
#        station_id = form.cleaned_data['station'].id
#        sensor_id = form.cleaned_data.get('sensor').id if form.cleaned_data.get('sensor') else None
#        start_date = form.cleaned_data['start_date']
#        end_date = form.cleaned_data['end_date']
#        
#        print(station_id)
#        print(sensor_id)
#        print(start_date)
#        
#        # Obtener los sensores asociados a la estación seleccionada
#        sensors = Sensor.objects.filter(stationID=station_id)
#        if sensor_id:
#            sensors = sensors.filter(id=sensor_id)
#
#        # Crear un diccionario para almacenar las mediciones por sensor
#        measurements_by_sensor = {}
#        
#        # Obtener las mediciones relacionadas con esos sensores y el rango de fechas
#        for sensor in sensors:
#            measurements = Measurements.objects.filter(
#                sensorID=sensor,
#                timestamp__gte=start_date,
#                timestamp__lte=end_date
#            )
#            # Almacena las mediciones en el diccionario usando el sensor como clave
#            measurements_by_sensor[sensor] = measurements
#        
#        # Puedes pasar 'measurements_by_sensor' a tu plantilla y usar Datatables para mostrar los datos
#        return self.render_to_response(self.get_context_data(form=form, measurements_by_sensor=measurements_by_sensor))
#    
#    def get_context_data(self, **kwargs):      
#        context = super().get_context_data(**kwargs)
#        context['user_stations'] = Station.objects.filter(user_ID=self.request.user)
#        context['subTitle'] = "Reports"
#        user = self.request.user
#        context['user_name'] = user.username
#        return context
#



class AlarmListView(LoginRequiredMixin, ListView):
    model = Alarm
    template_name = 'alarms.html'  # Cambia esto al nombre de tu plantilla HTML
    context_object_name = 'alarms'
    paginate_by = 10  # Si deseas paginación

    def get_queryset(self):
        # Obtener las estaciones relacionadas con el usuario logeado
        user = self.request.user
        stations = Station.objects.filter(user_ID=user)
        # Obtener los sensores relacionados con las estaciones
        sensors = Sensor.objects.filter(stationID__in=stations)
        # Filtrar las alarmas por el campo "alarm_type" igual a "alarm"
        alarms = Alarm.objects.filter(sensor__in=sensors, alarm_type='alarm')
        return alarms
    
    def get_context_data(self, **kwargs):
        #traemos el context desde el origen
        context = super().get_context_data(**kwargs)
        user = self.request.user
        #Agregamos información al context
        user_stations = Station.objects.filter(user_ID=self.request.user)
        # filtradas las alarmas relacionadas al usuario logeado
        user_sensor_alarms = Alarm.objects.filter(sensor__stationID__user_ID=user)
        #filtramos el tipo de alarmas
        user_alarms = user_sensor_alarms.filter(alarm_type='alarm')
        #user_warning = user_sensor_alarms.filter(alarm_type='warning').count()
        user_warning = user_sensor_alarms.filter(alarm_type='warning')
        context['title'] = "Alarms"
        context['user_stations']= user_stations
        context['user_name'] = user.username
        context['user_alarms'] = user_alarms
        context['user_warnings'] = user_warning
        context['subTitle'] = "List of Alarms"
        return context


class WarningListView(LoginRequiredMixin, ListView):
    model = Alarm
    template_name = 'warnings.html'  # Cambia esto al nombre de tu plantilla HTML
    context_object_name = 'warningss'
    #paginate_by = 5  # Si deseas paginación

    def get_queryset(self):
        # Obtener las estaciones relacionadas con el usuario logeado
        user = self.request.user
        stations = Station.objects.filter(user_ID=user)
        # Ajusta el campo owner según tu modelo de usuario
        # Obtener los sensores relacionados con las estaciones
        sensors = Sensor.objects.filter(stationID__in=stations)
        # Filtrar las alarmas por el campo "alarm_type" igual a "alarm"
        alarms = Alarm.objects.filter(sensor__in=sensors, alarm_type='warning')
        return alarms
    
    def get_context_data(self, **kwargs):
        #traemos el context desde el origen
        context = super().get_context_data(**kwargs)
        user = self.request.user
        #Agregamos información al context
        user_stations = Station.objects.filter(user_ID=self.request.user)
        # filtradas las alarmas relacionadas al usuario logeado
        user_sensor_alarms = Alarm.objects.filter(sensor__stationID__user_ID=user)
        #filtramos el tipo de alarmas
        user_alarms = user_sensor_alarms.filter(alarm_type='alarm')
        #user_warning = user_sensor_alarms.filter(alarm_type='warning').count()
        user_warning = user_sensor_alarms.filter(alarm_type='warning')
        context['title'] = "Warnings"
        context['user_stations']= user_stations
        context['user_name'] = user.username
        context['user_alarms'] = user_alarms
        context['user_warnings'] = user_warning
        context['subTitle'] = "List of Warnings"
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('Dashboard')  # 'profile' should be replaced with the name of the URL pattern for the user's profile

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_name'] = user.username
        context['subTitle'] = "Edit Profile"

        user_stations = Station.objects.filter(user_ID=self.request.user)
        # filtradas las alarmas relacionadas al usuario logeado
        user_sensor_alarms = Alarm.objects.filter(sensor__stationID__user_ID=user)
        #filtramos el tipo de alarmas
        user_alarms = user_sensor_alarms.filter(alarm_type='alarm')
        #user_warning = user_sensor_alarms.filter(alarm_type='warning').count()
        user_warning = user_sensor_alarms.filter(alarm_type='warning')
        context['title'] = "Profile"
        context['user_stations']= user_stations
        context['user_alarms'] = user_alarms
        context['user_warnings'] = user_warning




        return context