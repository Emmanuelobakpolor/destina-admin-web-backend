from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

class TransportCompany(models.Model):
    name = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)  # Vehicle plate number
    vehicle_image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)  # Image of vehicle plate number
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name


class Route(models.Model):
    company = models.ForeignKey(TransportCompany, related_name='routes', on_delete=models.CASCADE)
    departure_terminal = models.CharField(max_length=255)
    destination_terminal = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.departure_terminal} → {self.destination_terminal} ({self.company.name})"


class HostTrip(models.Model):
    startpoint = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
    departure_time = models.TimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    route_description = models.TextField(blank=True, null=True)
    assigned_bus = models.ImageField(upload_to='bus_images/', blank=True, null=True)  # Pic of the bus
    company = models.ForeignKey(TransportCompany, related_name='host_trips', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.startpoint} → {self.endpoint} ({self.company.name})"


RESERVATION_TYPE_CHOICES = (
    ('one_way', 'One Way'),
    ('round_trip', 'Round Trip'),
)

RESERVATION_STATUS_CHOICES = (
    ('confirmed', 'Confirmed'),
    ('pending', 'Pending'),
    ('declined', 'Declined'),
)

class Reservation(models.Model):
    customer_name = models.CharField(max_length=255)
    vehicle_image = models.ImageField(upload_to='reservation_vehicle_images/', blank=True, null=True)
    customer_phone = models.CharField(max_length=20)
    route = models.ForeignKey(Route, related_name='reservations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    reservation_type = models.CharField(max_length=20, choices=RESERVATION_TYPE_CHOICES, default='one_way')
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reservation by {self.customer_name} on {self.date}"
