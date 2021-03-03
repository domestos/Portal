from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView 
from django.views import View
from .forms import UpdateTicketStatusForm , CommentForm
  
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import TicketForm
from .models import Ticket, FollowUp
from .permissions import OwnerOrMembersPermissionsMixin, OwnerMembersPermissionsMixin
# Create your views here.



class RequestUser(LoginRequiredMixin):
    """ Check if user is auth and initialization the requested user """
    request_user = None
    permission_required = 'ticket.helpdesk_admin'

    def get_queryset(self):
        self.request_user = self.request.user
        return super().get_queryset()



#============================= LIST VIEW  =======================================================
class TicketListView(RequestUser, ListView):
    """ Get all tickets for superuser and own tickets for the user """
    model = Ticket
    template_name='ticket/list_ticket.html'

    def get_context_data(self, *args, **kwargs):
        context_object_name = super().get_context_data( *args, **kwargs)
        context_object_name['tickets'] = self.model.objects.all_or_created_by(self.request_user, self.permission_required)
        return context_object_name



def list_ticket(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'ticket/list_ticket.html',  {'tickets': tickets})
#==================================================================================================



#============================= CREATE  =======================================================
class TicketCreateView(RequestUser, CreateView):
    model = Ticket
    template_name = 'ticket/create_ticket.html'
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



#============================= DETAIL  =======================================================
class TicketDetailView(LoginRequiredMixin,OwnerMembersPermissionsMixin,  UpdateView):
    model = Ticket
    template_name = 'ticket/detail_ticket.html'
    permission_required = 'ticket.helpdesk_admin'
    
    def get_object(self):
        try:
            obj = Ticket.objects.get(pk=self.kwargs['pk'])
        except Question.DoesNotExist:
            raise Http404('Ticket not found!')
        return obj

    def get_context_data(self, **kwargs):
        kwargs['object'] = self.get_object()
        if 'update_ticket_form' not in kwargs:
            kwargs['update_ticket_form'] = UpdateTicketStatusForm(instance=self.get_object())
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = CommentForm()
        return kwargs

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        ctxt = {}

        if 'update_ticket' in request.POST:
            bound_update_ticket_form = UpdateTicketStatusForm(request.POST, instance=self.get_object())

            if bound_update_ticket_form.is_valid():
                    # Here, save the response
                    # check if form was edited (if bound form has values)
                    if (bound_update_ticket_form.changed_data):
                        msg = ''
                        for field in bound_update_ticket_form.changed_data:
                            old_value = self.get_object().__getattribute__(field)
                            new_value = bound_update_ticket_form.cleaned_data[field]
                            msg += f"<br> <b>{field}</b> from {old_value} to {new_value}"
                            print ( bound_update_ticket_form.cleaned_data[field]) 
                            print(msg)
                        comment = FollowUp()
                        comment.ticket=self.get_object()
                        comment.comment = msg
                        comment.user = self.request.user
                        comment.save()        

                    # for item  in self.get_object().__dict__.items():
                    #     print(item)


                    bound_update_ticket_form.save()
            else:
                ctxt['update_ticket_form'] = update_ticket_form

        elif 'comment_ticket' in request.POST:

            bound_comment_form = CommentForm(request.POST)

            if bound_comment_form.is_valid():
                    # Here, save the comment
                    comment = FollowUp()
                    comment.ticket=self.get_object()
                    comment.comment = bound_comment_form.cleaned_data['comment']
                    comment.user = self.request.user
                    comment.save()
                    return redirect('detail_ticket', self.kwargs['pk'])
            else:
                ctxt['comment_form'] = comment_form

        return render(request, self.template_name, self.get_context_data(**ctxt))


class TicketDetailView2(LoginRequiredMixin, OwnerMembersPermissionsMixin, UpdateView):
    model = Ticket
    template_name = 'ticket/detail_ticket.html'
    permission_required = 'ticket.helpdesk_admin'
    permission_denied_message = 'ZHOPA'
    form_class = UpdateTicketStatusForm 
    success_url = '/ticket/'

    def form_valid(self, form): 
        # This method is called when valid form data has been POSTed. 
        # It should return an HttpResponse. 
          
        # perform a action here 
        print(form.cleaned_data) 
        print (dir(self))
        return super().form_valid(form) 

def view_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if (ticket.created_by == request.user or request.user.is_superuser):
        return render(request, 'ticket/detail_ticket.html', {})

    return redirect('list_ticket')
        



#         # views.py
# def _get_form(request, formcls, prefix):
#     data = request.POST if prefix in request.POST else None
#     return formcls(data, prefix=prefix)

# class MyView(TemplateView):
#     template_name = 'mytemplate.html'

#     def get(self, request, *args, **kwargs):
#         return self.render_to_response({'aform': AForm(prefix='aform_pre'), 'bform': BForm(prefix='bform_pre')})

#     def post(self, request, *args, **kwargs):
#         aform = _get_form(request, AForm, 'aform_pre')
#         bform = _get_form(request, BForm, 'bform_pre')
#         if aform.is_bound and aform.is_valid():
#             # Process aform and render response
#         elif bform.is_bound and bform.is_valid():
#             # Process bform and render response
#         return self.render_to_response({'aform': aform, 'bform': bform})

# # mytemplate.html
# <form action="" method="post">
#     {% csrf_token %}
#     {{ aform.as_p }}
#     <input type="submit" name="{{aform.prefix}}" value="Submit" />
#     {{ bform.as_p }}
#     <input type="submit" name="{{bform.prefix}}" value="Submit" />
# </form>
#============================= UPDATE  =======================================================