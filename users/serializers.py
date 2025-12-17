from rest_framework import serializers
from .models import Route, TransportCompany, User, HostTrip, Reservation
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'company', 'departure_terminal', 'destination_terminal']

class TransportCompanySerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = TransportCompany
        fields = ['id', 'name', 'vehicle_number', 'vehicle_image', 'date_joined', 'status', 'routes']

class HostTripSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = HostTrip
        fields = [
            'id', 'startpoint', 'endpoint', 'departure_time', 'amount',
            'route_description', 'assigned_bus', 'company', 'company_name',
            'date_joined', 'status'
        ]

class ReservationSerializer(serializers.ModelSerializer):
    route_details = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'customer_name', 'vehicle_image', 'customer_phone',
            'route', 'route_details', 'amount', 'date', 'time',
            'reservation_type', 'status'
        ]

    def get_route_details(self, obj):
        return {
            'departure_terminal': obj.route.departure_terminal,
            'destination_terminal': obj.route.destination_terminal,
            'company': obj.route.company.name
        }
