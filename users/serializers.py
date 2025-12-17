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
    route_details = RouteSerializer(source='route', read_only=True)
    transport_company_name = serializers.CharField(source='transport_company.company_name', read_only=True)

    class Meta:
        model = HostTrip
        fields = [
            'id', 'transport_company', 'transport_company_name', 'route', 'route_details',
            'departure_date', 'departure_time', 'available_seats', 'vehicle_image', 'date_joined'
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
            'origin': obj.host_trip.route.origin,
            'destination': obj.host_trip.route.destination,
            'company': obj.host_trip.transport_company.company_name
        }
