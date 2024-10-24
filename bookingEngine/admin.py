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

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'requires_agent', 'created_at')
    list_filter = ('requires_agent', 'company')
    search_fields = ('name', 'company__name')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'email', 'company__name')

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'company', 'price', 'duration', 'is_active')
    list_filter = ('is_active', 'type', 'company')
    search_fields = ('name', 'company__name')
    inlines = [ScheduleInline]
    filter_horizontal = ('agents',)

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

@admin.register(BlockedTime)
class BlockedTimeAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'start_datetime', 'end_datetime', 'reason')
    list_filter = ('start_datetime',)
    search_fields = ('resource__name', 'agent__name', 'reason')
    
    def get_name(self, obj):
        return obj.resource.name if obj.resource else obj.agent.name
    get_name.short_description = 'Recurso/Agente'