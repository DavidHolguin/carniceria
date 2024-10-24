from django.contrib import admin
from .models import (
    BookingSettings, ResourceType, Agent, Resource,
    Schedule, Booking, BlockedTime
)

@admin.register(BookingSettings)
class BookingSettingsAdmin(admin.ModelAdmin):
    list_display = ('company', 'google_calendar_enabled', 'automatic_confirmation', 'created_at')
    list_filter = ('google_calendar_enabled', 'automatic_confirmation')
    search_fields = ('company__name',)
    fieldsets = (
        ('Información General', {
            'fields': ('company', 'notification_email')
        }),
        ('Configuración de Google Calendar', {
            'fields': ('google_calendar_enabled', 'google_calendar_credentials'),
            'classes': ('collapse',),
            'description': 'Configuración para la integración con Google Calendar'
        }),
        ('Reglas de Reserva', {
            'fields': ('advance_booking_limit', 'cancellation_limit_hours', 'automatic_confirmation'),
            'description': 'Configuración de las reglas generales para las reservas'
        }),
    )

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'requires_agent', 'created_at')
    list_filter = ('requires_agent', 'company')
    search_fields = ('name', 'company__name')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'company', 'description')
        }),
        ('Configuración', {
            'fields': ('requires_agent',),
            'description': 'Configuración específica del tipo de recurso'
        }),
    )

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'email', 'company__name')
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Información Empresarial', {
            'fields': ('company', 'user', 'is_active')
        }),
    )

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'company', 'price', 'duration', 'is_active')
    list_filter = ('is_active', 'type', 'company')
    search_fields = ('name', 'company__name')
    inlines = [ScheduleInline]
    filter_horizontal = ('agents',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'type', 'company', 'description')
        }),
        ('Detalles del Servicio', {
            'fields': ('price', 'duration', 'availability_type')
        }),
        ('Configuración de Agentes', {
            'fields': ('agents', 'is_active'),
            'description': 'Asignación de agentes y estado del recurso'
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    
    def get_name(self, obj):
        return obj.resource.name if obj.resource else obj.agent.name
    get_name.short_description = 'Recurso/Agente'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'resource', 'agent', 'start_datetime', 'end_datetime', 'status')
    list_filter = ('status', 'resource__company', 'start_datetime')
    search_fields = ('user__username', 'resource__name', 'agent__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('user', 'resource', 'agent')
        }),
        ('Horario', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Estado', {
            'fields': ('status', 'notes')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BlockedTime)
class BlockedTimeAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_datetime', 'end_datetime', 'reason')
    list_filter = ('start_datetime',)
    search_fields = ('resource__name', 'agent__name', 'reason')
    
    def get_name(self, obj):
        return obj.resource.name if obj.resource else obj.agent.name
    get_name.short_description = 'Recurso/Agente'
    
    fieldsets = (
        ('Asignación', {
            'fields': ('resource', 'agent'),
            'description': 'Seleccione un recurso O un agente, no ambos'
        }),
        ('Período', {
            'fields': ('start_datetime', 'end_datetime', 'reason')
        }),
    )