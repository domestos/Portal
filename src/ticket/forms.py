from django import forms
from .models import Ticket, FollowUp

class TicketForm(forms.ModelForm):
    due_date = forms.DateTimeField
    class Meta:
        model = Ticket
        fields = ( 'priority', 'cc', 'subject', 'text', 'due_date')
        # widgets = {
        #            'due_date': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
        #         #    'field1': forms.TextInput(attrs={'class':'textInputClass', 'placeholder':'Enter a Value..'}),
        #         #    'field2': forms.TextInput(attrs={'class':'textInputClass', 'placeholder':'Enter a Value..', 'readonly':'readonly', 'value':10}),
        #         #    'desc': forms.Textarea(attrs={'class':'textAreaInputClass', 'placeholder':'Enter desc', 'rows':5}),

        #        }

class UpdateTicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('progress','priority')


class CommentForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ( 'comment',)

    def save(self, *args, **kwargs):
        print(kwargs)
        return super().save(self, *args, **kwargs)
