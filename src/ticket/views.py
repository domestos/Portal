from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView 
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
# Models 
from .models import Ticket, FollowUp
# Forms 
from .forms import TicketForm,UpdateTicketStatusForm , CommentForm
from .service_mixin import MultipleForms  
# Permissions 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Custom Permissions 
from .permissions import OwnerOrMembersPermissionsMixin, OwnerMembersPermissionsMixin
# eamil
from .email import SendEmailNewTicket
# Table 
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView
from .tables import PersonTable
# Create your views here.


#============================= LIST VIEW  =======================================================
class TicketListView(LoginRequiredMixin, SingleTableView):
    """ Get all tickets for superuser and own tickets for the user """
    model = Ticket
    template_name='ticket/list_ticket.html'
    permission_required = 'ticket.helpdesk_admin'
    request_user = None
    table_class = PersonTable
    

    def get_context_data(self, *args, **kwargs):
        context_object_name = super().get_context_data( *args, **kwargs)
        context_object_name['tickets'] = self.model.objects.all_or_created_by(self.request.user, self.permission_required)
        return context_object_name



def list_ticket(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'ticket/list_ticket.html',  {'tickets': tickets})
#==================================================================================================



#============================= CREATE  ============================================================
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'ticket/create_ticket.html'
    fields = ['priority', 'cc', 'subject', 'text', 'due_date']
    success_url = reverse_lazy('list_ticket')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        new_ticket = form.save()
        SendEmailNewTicket(self.request, new_ticket, new_ticket.text).sendEmail()
        return super().form_valid(form)
#==================================================================================================



#============================= DETAIL AND UPDATE =================================================
class TicketDetailView(LoginRequiredMixin, OwnerOrMembersPermissionsMixin,  MultipleForms):
    """ Display detail ticket and change ticket detail or add a comment. 
        OwnerOrMembersPermissionsMixin -> allow access for users: owner, members, and helpdesk_admin
        MultipleForms -> manage two forms: CommentForm and UpdateTicketForm """
    model = Ticket
    template_name = 'ticket/detail_ticket.html'
    permission_required = 'ticket.helpdesk_admin'
    
#==================================================================================================