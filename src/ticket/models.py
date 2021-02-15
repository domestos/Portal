from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Ticket (models.Model):
    PROGRESS_CHOICES = (
        ( 'not_started', 'Not started' ),
        ( 'in_progress', 'In progress' ),
        ( 'completed'  , 'Completed' ),
    )

    PRIORITY_CHOICES = (
        ('urgent' , 'Urgent'),
        ('important' , 'Important'),
        ('medium' , 'Medium'),
        ('low' , 'Low'),
    )
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
   
    progress = models.CharField(
        _('Progress'), 
        max_length = 20,
        choices=PROGRESS_CHOICES, 
        default="not_started"
    )
   
    priority = models.CharField(
        _('Priority'), 
        max_length = 20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
  
    created = models.DateTimeField(
        _('Created'), 
        blank=True, 
        help_text=_('Date this ticket was first created')
    )
   
    modified = models.DateTimeField(
        _('Modified'),
        blank=True, 
        help_text=_('Date this ticket was most recently changed.'),
    )
  
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
        help_text=_('The content of the customers query.'),
    )

    due_date = models.DateTimeField(
        _('Due on'),
        blank=True,
        null=True,
    )



# class Attachment(models.Model):
#     """
#     Represents a file attached to a follow-up. This could come from an e-mail
#     attachment, or it could be uploaded via the web interface.
#     """

#     file = models.FileField(
#         _('File'),
#         upload_to=attachment_path,
#         max_length=1000,
#     )

#     filename = models.CharField(
#         _('Filename'),
#         blank=True,
#         max_length=1000,
#     )

#     mime_type = models.CharField(
#         _('MIME Type'),
#         blank=True,
#         max_length=255,
#     )

#     size = models.IntegerField(
#         _('Size'),
#         blank=True,
#         help_text=_('Size of this file in bytes'),
#     )

#     def __str__(self):
#         return '%s' % self.filename

#     def save(self, *args, **kwargs):

#         if not self.size:
#             self.size = self.get_size()

#         if not self.filename:
#             self.filename = self.get_filename()

#         if not self.mime_type:
#             self.mime_type = \
#                 mimetypes.guess_type(self.filename, strict=False)[0] or \
#                 'application/octet-stream'

#         return super(Attachment, self).save(*args, **kwargs)

#     def get_filename(self):
#         return str(self.file)

#     def get_size(self):
#         return self.file.file.size

#     def attachment_path(self, filename):
#         """Provide a file path that will help prevent files being overwritten, by
#         putting attachments in a folder off attachments for ticket/followup_id/.
#         """
#         assert NotImplementedError(
#             "This method is to be implemented by Attachment classes"
#         )

#     class Meta:
#         ordering = ('filename',)
#         verbose_name = _('Attachment')
#         verbose_name_plural = _('Attachments')
#         abstract = True

