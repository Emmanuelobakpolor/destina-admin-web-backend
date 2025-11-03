from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .models import User, TransportCompany, Route, HostTrip, Reservation
from .serializers import UserSerializer, TransportCompanySerializer, RouteSerializer, HostTripSerializer, ReservationSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TransportCompanyListCreateView(generics.ListCreateAPIView):
    queryset = TransportCompany.objects.all().order_by('-date_joined')
    serializer_class = TransportCompanySerializer
    permission_classes = [permissions.AllowAny]


class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]


class HostTripListCreateView(generics.ListCreateAPIView):
    queryset = HostTrip.objects.all().order_by('-date_joined')
    serializer_class = HostTripSerializer
    permission_classes = [permissions.AllowAny]


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('-date')
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]


class ReservationApprovalView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action')  # 'approve' or 'decline'
        if action == 'approve':
            instance.status = 'confirmed'
        elif action == 'decline':
            instance.status = 'declined'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReservationReceiptView(generics.RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Generate receipt data
        receipt = {
            'receipt_number': f"REC-{instance.id}",
            'customer_name': data['customer_name'],
            'customer_phone': data['customer_phone'],
            'route': data['route_details'],
            'amount': data['amount'],
            'date': data['date'],
            'time': data['time'],
            'reservation_type': data['reservation_type'],
            'status': data['status'],
            'vehicle_image': data['vehicle_image']
        }
        return Response(receipt)
