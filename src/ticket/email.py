from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

# def _get_full_path_to_ticket(request):
#     return f"{request.scheme}://{request.get_host()}{request.path}"

# def _get_cc_emails(ticket):
#     cc = []
#     for user in ticket.cc.all():
#         if user.email:
#             cc.append(user.email)
#     return cc 

# def _get_created_by_email(ticket):
#     return ticket.created_by.email

# def sendEmail(request, ticket, comment):
#     ticket_link = _get_full_path_to_ticket(request)
#     email_template ='ticket/email_template.html'
#     subject =   'HelpDesk Ticket #'+str(ticket.id), 
#     email_body = render_to_string( email_template, {'name':request.user.username, 'ticket':ticket, 'ticket_link':ticket_link, 'comment':comment})
 
#     email = EmailMultiAlternatives(
#         subject,
#         email_body,
#         settings.EMAIL_HOST_USER, 
#         _get_created_by_email(ticket), 
#         cc=_get_cc_emails(ticket))
#     email.attach_alternative(email_body, "text/html")
#     email.fail_silently=False
#     email.send()


class BaseSendMail:
    request = None
    ticket = None
    comment = None
    html_email_template = None
    text_email_template = None
    
    def __init__(self, request, ticket, comment):
        self.request = request
        self.ticket = ticket
        self.comment = comment
        # self.sendEmail()
       
    def _get_full_path_to_ticket(sefl, request):
        return f"{request.scheme}://{request.get_host()}{request.path}"

    def _get_cc_emails(self):
        cc = []
        for user in self.ticket.cc.all():
            if user.email:
                cc.append(user.email)
        return cc 

    def _get_created_by_email(self):
        return  self.ticket.created_by.email

    def _get_subject(self):
        return f"HelpDesk Ticket #{self.ticket.id}: {self.ticket.subject} "

    def sendEmail(self):
        context = {
            'name':self.request.user.username, 
            'ticket':self.ticket, 
            'ticket_link':self._get_full_path_to_ticket(self.request), 
            'comment':self.comment
            }
        html_body = render_to_string(self.html_email_template, context)

        text_body = render_to_string(self.text_email_template, context)

        email = EmailMultiAlternatives(
            self._get_subject(),
            text_body,
            settings.EMAIL_HOST_USER, 
            [self._get_created_by_email(),],
            cc=self._get_cc_emails()
            )
        email.attach_alternative(html_body, "text/html")
        email.fail_silently=False
        email.send()

class SendEmailTicketWasChanged(BaseSendMail):
    html_email_template ='ticket/email_templates/html_ticket_changed.html'
    text_email_template ='ticket/email_templates/text_ticket_changed.html'

class SendEmailComment(BaseSendMail):
    html_email_template ='ticket/email_templates/html_ticket_comment.html'
    text_email_template ='ticket/email_templates/text_ticket_comment.html'

class SendEmailNewTicket(BaseSendMail):
    html_email_template ='ticket/email_templates/html_ticket_created.html'
    text_email_template ='ticket/email_templates/text_ticket_created.html'

    # def _create_message (subject, text_body, html_body, from_email, email_to):
    #     if not text_body and not html_body:
    #         raise ValueError(_('Either text_body or html_body should be not None'))

    #     return {'subject':subject, 'body': html_body, 'from_email':from_email. 'to':email_to}

    # def sendEmail(self):
    #     connection = mail.get_connection()
    #     connection.open()
    #     cc_email = EmailMultiAlternatives(
    #         self._get_subject(),
    #         text_body,
    #         settings.EMAIL_HOST_USER, 
    #         self._get_created_by_email(), 
    #         cc=self._get_cc_emails()
    #         )