from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta


class BookingSettings(models.Model):
    """Configuración global del sistema de reservas para una empresa"""
    company = models.ForeignKey('marketplace.Company', on_delete=models.CASCADE)
    google_calendar_enabled = models.BooleanField(default=False)
    google_calendar_credentials = models.JSONField(null=True, blank=True)
    notification_email = models.EmailField(null=True, blank=True)
    advance_booking_limit = models.IntegerField(
        default=30,
        help_text="Días máximos de anticipación para reservar"
    )
    cancellation_limit_hours = models.IntegerField(
        default=24,
        help_text="Horas límite para cancelar una reserva"
    )
    automatic_confirmation = models.BooleanField(
        default=False,
        help_text="Confirmar reservas automáticamente"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de Reservas"
        verbose_name_plural = "Configuraciones de Reservas"

class ResourceType(models.Model):
    """Tipo de recurso reservable (Servicio, Habitación, Mesa, etc)"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey('marketplace.Company', on_delete=models.CASCADE)
    requires_agent = models.BooleanField(
        default=True,
        help_text="¿Requiere un agente para el servicio?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Agent(models.Model):
    """Agentes que pueden ser asignados a recursos y reservas"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey('marketplace.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"

    class Meta:
        unique_together = ['company', 'email']

class Resource(models.Model):
    """Recurso reservable (un servicio específico, una habitación, una mesa, etc)"""
    AVAILABILITY_CHOICES = [
        ('always', 'Siempre disponible'),
        ('schedule', 'Según horario'),
        ('custom', 'Personalizado'),
    ]
    
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    company = models.ForeignKey('marketplace.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(
        help_text="Duración en minutos",
        validators=[MinValueValidator(1)]
    )
    availability_type = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='schedule'
    )
    agents = models.ManyToManyField(Agent, related_name='resources', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Schedule(models.Model):
    """Horarios de disponibilidad para recursos y agentes"""
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = [
            ['resource', 'day_of_week'],
            ['agent', 'day_of_week']
        ]

    def clean(self):
        if not self.resource and not self.agent:
            raise ValidationError('Debe especificar un recurso o un agente')
        if self.resource and self.agent:
            raise ValidationError('No puede especificar ambos: recurso y agente')
        if self.start_time >= self.end_time:
            raise ValidationError('La hora de inicio debe ser anterior a la hora de fin')

class Booking(models.Model):
    """Reservas de recursos"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_datetime']
        
    def clean(self):
        if self.resource.type.requires_agent and not self.agent:
            raise ValidationError('Este tipo de recurso requiere un agente asignado')
            
        if self.start_datetime >= self.end_datetime:
            raise ValidationError('La hora de inicio debe ser anterior a la hora de fin')
            
        # Verificar disponibilidad
        overlapping_bookings = Booking.objects.filter(
            resource=self.resource,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime,
            status='confirmed'
        ).exclude(id=self.id)
        
        if overlapping_bookings.exists():
            raise ValidationError('El recurso no está disponible en este horario')
            
        if self.agent:
            agent_bookings = Booking.objects.filter(
                agent=self.agent,
                start_datetime__lt=self.end_datetime,
                end_datetime__gt=self.start_datetime,
                status='confirmed'
            ).exclude(id=self.id)
            
            if agent_bookings.exists():
                raise ValidationError('El agente no está disponible en este horario')

class BlockedTime(models.Model):
    """Períodos bloqueados para recursos o agentes"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if not self.resource and not self.agent:
            raise ValidationError('Debe especificar un recurso o un agente')
        if self.resource and self.agent:
            raise ValidationError('No puede especificar ambos: recurso y agente')
        if self.start_datetime >= self.end_datetime:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin')