from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def approved_distributor_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = getattr(request.user, 'distributor_profile', None)
        if profile and profile.is_approved:
            return view_func(request, *args, **kwargs)
        messages.warning(request, 'Your distributor account is pending approval or does not have access to the portal yet.')
        return redirect('distributors:registration_status')

    return _wrapped_view