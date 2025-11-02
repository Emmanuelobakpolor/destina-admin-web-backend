from django.urls import path
from .views import (
    RouteListCreateView, SignupView, LoginView, TransportCompanyListCreateView,
    HostTripListCreateView, ReservationListCreateView, ReservationApprovalView, ReservationReceiptView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    path('companies/', TransportCompanyListCreateView.as_view(), name='companies'),
    path('routes/', RouteListCreateView.as_view(), name='routes'),
    path('host-trips/', HostTripListCreateView.as_view(), name='host-trips'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservations'),
    path('reservations/<int:pk>/approve/', ReservationApprovalView.as_view(), name='reservation-approve'),
    path('reservations/<int:pk>/receipt/', ReservationReceiptView.as_view(), name='reservation-receipt'),
]
