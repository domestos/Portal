from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import FollowUp
from .forms import UpdateTicketStatusForm , CommentForm
#form mail 

from .email import  SendEmailTicketWasChanged, SendEmailComment

class MultipleForms(UpdateView):
    """  For each FollowUp, any changes to the ticket or add a commit are tracked here for display purposes..  """
    model = None
    ticket = None 

    def get_object(self):
        self.ticket = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return self.ticket

    def get_context_data(self, **kwargs):
        kwargs['object'] = self.ticket
        if 'update_ticket_form' not in kwargs:
            kwargs['update_ticket_form'] = UpdateTicketStatusForm(instance=self.ticket)
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = CommentForm()
        return kwargs

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name, self.get_context_data())

    def _save_comment(self, request, comment, title):
        FollowUp(ticket=self.ticket, title=title, comment=comment, user=request.user).save()

    def _save_ticket_changes_to_comment(self, request, bound_form):
        # check if form was edited (if bound form has values)
        if (bound_form.changed_data):
            comment = ''
            for field in bound_form.changed_data:
                old_value = self.get_object().__getattribute__(field)
                new_value = bound_form.cleaned_data[field]
                comment += f"Changed {field}: {old_value} --> {new_value} <br>"
            self._save_comment(request, comment, 'Changed')
            SendEmailTicketWasChanged(request, self.ticket, comment).sendEmail()

    def post(self, request, *args, **kwargs):
        ctxt = {}
        if 'update_ticket' in request.POST:
            bound_form_ticket = UpdateTicketStatusForm(request.POST, instance=self.ticket)
            if bound_form_ticket.is_valid() and bound_form_ticket.changed_data:
                self._save_ticket_changes_to_comment(request, bound_form_ticket)
                bound_form_ticket.save()
                return redirect('detail_ticket', self.kwargs['pk'])
            else:
                ctxt['update_ticket_form'] = bound_form_ticket

        elif 'comment_ticket' in request.POST:
            bound_form_comment = CommentForm(request.POST)
            if bound_form_comment.is_valid():
                # Here, save the comment
                comment=bound_form_comment.cleaned_data['comment']
                self._save_comment(request, comment, 'Comment')
                SendEmailComment(request, self.ticket, comment).sendEmail()
                return redirect('detail_ticket', self.kwargs['pk'])
            else:
                ctxt['comment_form'] = comment_form

        return render(request, self.template_name, self.get_context_data(**ctxt))
