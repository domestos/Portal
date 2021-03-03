from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import  PermissionRequiredMixin


#====================== SIMPLE CUSTOM PERMISSIONS CLASSES (is not used now )=========================
class CreatedByPermissionsMixin:
    def has_permissions(self):
        return self.get_object().created_by == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class OwnerOrMembersPermissionsMixin(CreatedByPermissionsMixin):
    def has_permissions(self):
        return self.request.user in self.get_object().cc.all() or self.get_object().created_by == self.request.user or self.request.user.has_perm(self.permission_required)

#====================================================================================

#================== CUSTOM PERMISSION ===============================================
class OwnerMembersPermissionsMixin(PermissionRequiredMixin):
    """
    Allow access for owner, members of cc and users who have permission 'ticket.helpdesk_admin'
    WARNING: this class works only with DetailView (where exists method get_object() )
    """    
    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user in self.get_object().cc.all() or self.get_object().created_by == self.request.user or self.request.user.has_perm(perms)
