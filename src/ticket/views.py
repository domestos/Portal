from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import  ListView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import TicketForm
from .models import Ticket
# Create your views here.

#============================= LIST VIEW  =======================================================
class RequestUser(LoginRequiredMixin):
    """ Checking if user is auth and initialization the requested user """
    request_user = None

    def get_queryset(self):
        self.request_user = self.request.user



class TicketListView(RequestUser, ListView):
    """ Getting all tickets for superuser and own tickets for the user """
    model =Ticket
    template_name='ticket/list_ticket.html'

    def get_context_data(self, *args, **kwargs):
        context_object_name = super().get_context_data( *args, **kwargs)
        context_object_name['tickets'] = self.model.objects.all_or_created_by(self.request_user)
        return context_object_name




def list_ticket(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'ticket/list_ticket.html',  {'tickets': tickets})
#==================================================================================================



#============================= CREATE  =======================================================
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name='ticket/create_ticket.html'
    fields = ['priority', 'cc', 'subject', 'text', 'due_date']
    success_url = reverse_lazy('list_ticket')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# this function is the same as the top class
def create_ticket(request):
    ticket_form = TicketForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.created_by = request.user
            new_ticket.save()
            return redirect('list_ticket')
    else:
        ticket_form = TicketForm()
    return render(request, 'ticket/create_ticket.html', {'form': ticket_form})
#==================================================================================================

def view_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if (ticket.created_by == request.user or request.user.is_superuser):
        return render(request, 'ticket/view_ticket.html', {})

    return redirect('list_ticket')
        
