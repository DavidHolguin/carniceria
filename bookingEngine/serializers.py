from rest_framework import serializers
from .models import (
    BookingSettings, ResourceType, Agent, Resource, 
    Schedule, Booking, BlockedTime
)
from django.utils import timezone
from datetime import timedelta



class BookingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSettings
        fields = '__all__'

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = Schedule
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True, read_only=True)
    agents = AgentSerializer(many=True, read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')
    
    def validate(self, data):
        # Validaciones adicionales para la reserva
        resource = data.get('resource')
        start_datetime = data.get('start_datetime')
        end_datetime = data.get('end_datetime')
        agent = data.get('agent')

        # Verificar que el recurso está activo
        if not resource.is_active:
            raise serializers.ValidationError("Este recurso no está disponible actualmente")

        # Verificar que la fecha no sea pasada
        if start_datetime < timezone.now():
            raise serializers.ValidationError("No se pueden hacer reservas en fechas pasadas")

        # Verificar límite de anticipación
        company_settings = BookingSettings.objects.get(company=resource.company)
        max_future_date = timezone.now() + timedelta(days=company_settings.advance_booking_limit)
        if start_datetime > max_future_date:
            raise serializers.ValidationError(
                f"Solo se pueden hacer reservas con {company_settings.advance_booking_limit} días de anticipación"
            )

        # Verificar disponibilidad
        if Booking.objects.filter(
            resource=resource,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime,
            status='confirmed'
        ).exists():
            raise serializers.ValidationError("El recurso no está disponible en este horario")

        if agent and Booking.objects.filter(
            agent=agent,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime,
            status='confirmed'
        ).exists():
            raise serializers.ValidationError("El agente no está disponible en este horario")

        return data

class BlockedTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedTime
        fields = '__all__'

# Serializers adicionales para vistas específicas
class ResourceAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    available_slots = serializers.ListField(
        child=serializers.DictField()
    )

class AgentAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    available_slots = serializers.ListField(
        child=serializers.DictField()
    )