from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from marketplace.models import Company
from datetime import datetime, timedelta
from .models import (
    BookingSettings, ResourceType, Agent, Resource, 
    Schedule, Booking, BlockedTime
)
from .serializers import (
    BookingSettingsSerializer, ResourceTypeSerializer,
    AgentSerializer, ResourceSerializer, ScheduleSerializer,
    BookingSerializer, BlockedTimeSerializer,
    ResourceAvailabilitySerializer
)

class IsCompanyOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es dueño de la empresa
    o administrador del sistema
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
            
        # Verificar si el usuario es dueño de alguna empresa
        return request.user.company_set.exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
            
        # Obtener la empresa relacionada con el objeto
        company = None
        if hasattr(obj, 'company'):
            company = obj.company
        elif hasattr(obj, 'resource'):
            company = obj.resource.company
            
        return company and company.user == request.user

class BookingSettingsViewSet(viewsets.ModelViewSet):
    queryset = BookingSettings.objects.all()
    serializer_class = BookingSettingsSerializer
    permission_classes = [IsCompanyOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return BookingSettings.objects.all()
        return BookingSettings.objects.filter(company__user=self.request.user)

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [IsCompanyOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ResourceType.objects.all()
        return ResourceType.objects.filter(company__user=self.request.user)
    
    def perform_create(self, serializer):
        company = get_object_or_404(Company, user=self.request.user)
        serializer.save(company=company)

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsCompanyOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Agent.objects.all()
        return Agent.objects.filter(company__user=self.request.user)
    
    def perform_create(self, serializer):
        company = get_object_or_404(Company, user=self.request.user)
        serializer.save(company=company)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        agent = self.get_object()
        date_param = request.query_params.get('date', datetime.now().date())
        
        if isinstance(date_param, str):
            date_param = datetime.strptime(date_param, '%Y-%m-%d').date()
        
        # Obtener horario del agente para ese día
        schedule = Schedule.objects.filter(
            agent=agent,
            day_of_week=date_param.weekday()
        ).first()
        
        if not schedule:
            return Response({
                'date': date_param,
                'available_slots': []
            })
            
        # Implementar lógica para obtener slots disponibles
        # basados en el horario y las reservas existentes
        # ...
        
        return Response({
            'date': date_param,
            'available_slots': []  # Implementar lógica de slots
        })

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsCompanyOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Resource.objects.all()
            
        company_resources = Resource.objects.filter(company__user=self.request.user)
        
        # Filtrar por tipo de recurso si se especifica
        resource_type = self.request.query_params.get('type')
        if resource_type:
            company_resources = company_resources.filter(type__id=resource_type)
            
        return company_resources
    
    def perform_create(self, serializer):
        company = get_object_or_404(Company, user=self.request.user)
        serializer.save(company=company)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        resource = self.get_object()
        date_param = request.query_params.get('date', datetime.now().date())
        
        if isinstance(date_param, str):
            date_param = datetime.strptime(date_param, '%Y-%m-%d').date()
        
        # Obtener configuración de la empresa
        settings = BookingSettings.objects.get(company=resource.company)
        
        # Verificar si la fecha está dentro del límite de anticipación
        max_future_date = timezone.now().date() + timedelta(days=settings.advance_booking_limit)
        if date_param > max_future_date:
            return Response({
                "error": f"Solo se pueden ver disponibilidad hasta {settings.advance_booking_limit} días en el futuro"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener horario del recurso para ese día
        schedule = Schedule.objects.filter(
            resource=resource,
            day_of_week=date_param.weekday()
        ).first()
        
        if not schedule:
            return Response({
                'date': date_param,
                'available_slots': []
            })
            
        # Implementar lógica para obtener slots disponibles
        # basados en el horario, duración del servicio y reservas existentes
        # ...
        
        return Response({
            'date': date_param,
            'available_slots': []  # Implementar lógica de slots
        })

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsCompanyOwnerOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Booking.objects.all()
            
        # Si el usuario es dueño de una empresa, mostrar todas las reservas de su empresa
        if user.company_set.exists():
            company = user.company_set.first()
            return Booking.objects.filter(resource__company=company)
            
        # Si es un usuario normal, mostrar solo sus reservas
        return Booking.objects.filter(user=user)
    
    def perform_create(self, serializer):
        # Verificar disponibilidad antes de crear la reserva
        resource = serializer.validated_data['resource']
        start_datetime = serializer.validated_data['start_datetime']
        end_datetime = serializer.validated_data['end_datetime']
        agent = serializer.validated_data.get('agent')
        
        # Verificar si el recurso pertenece a una empresa con reservas habilitadas
        if not hasattr(resource.company, 'bookingsettings'):
            raise PermissionDenied("Esta empresa no tiene habilitado el sistema de reservas")
        
        settings = resource.company.bookingsettings
        
        # Verificar si la reserva se realiza con la anticipación permitida
        max_future_date = timezone.now() + timedelta(days=settings.advance_booking_limit)
        if start_datetime.date() > max_future_date.date():
            raise PermissionDenied(
                f"Solo se pueden hacer reservas con {settings.advance_booking_limit} días de anticipación"
            )
        
        # Crear la reserva
        serializer.save(
            user=self.request.user,
            status='confirmed' if settings.automatic_confirmation else 'pending'
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        settings = booking.resource.company.bookingsettings
        
        # Verificar si está dentro del límite de cancelación
        if (booking.start_datetime - timezone.now()) < timedelta(hours=settings.cancellation_limit_hours):
            return Response({
                "error": f"No se puede cancelar con menos de {settings.cancellation_limit_hours} horas de anticipación"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'cancelled'
        booking.save()
        
        # Enviar notificaciones
        # ...
        
        return Response({'status': 'Reserva cancelada correctamente'})

class BlockedTimeViewSet(viewsets.ModelViewSet):
    queryset = BlockedTime.objects.all()
    serializer_class = BlockedTimeSerializer
    permission_classes = [IsCompanyOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return BlockedTime.objects.all()
        return BlockedTime.objects.filter(
            Q(resource__company__user=self.request.user) |
            Q(agent__company__user=self.request.user)
        )