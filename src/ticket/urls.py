# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.list_ticket, name='list_ticket'),
    path('', views.TicketListView.as_view(), name='list_ticket'),

    # path('create', views.create_ticket, name='create_ticket'),
    path('new', views.TicketCreateView.as_view(), name='create_ticket'),

#    path('view/<int:pk>', views.view_ticket, name='view_ticket'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='detail_ticket'),

    # add new url for admin list, and detail view

]