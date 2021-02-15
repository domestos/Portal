from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import TicketForm
from .models import Ticket
# Create your views here.

def list_ticket(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'ticket/list_ticket.html',  {'tickets': tickets})


def create_ticket(request):
    ticket_form = TicketForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('list_ticket')
    else:
        ticket_form = TicketForm()
    return render(request, 'ticket/create_ticket.html', {'form': ticket_form})


def view_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if (ticket.user == request.user or request.user.is_superuser):
        return render(request, 'ticket/view_ticket.html', {})

    return redirect('list_ticket')
        
