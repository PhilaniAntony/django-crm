from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganisorRequiredMixixn(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.is_agent:
            return redirect('leads:homepage')
        return super().dispatch(request, *args, **kwargs)
