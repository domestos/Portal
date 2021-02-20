# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.list_ticket, name='list_ticket'),
    path('', views.TicketListView.as_view(), name='list_ticket'),

    # path('create', views.create_ticket, name='create_ticket'),
    path('create', views.TicketCreateView.as_view(), name='create_ticket'),
    path('view/<int:pk>', views.view_ticket, name='view_ticket'),
]