from django.http import HttpResponseForbidden
from functools import wraps

def vendor_or_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is either a vendor (is_seller) or an admin (is_superuser)
        if not (getattr(request.user, 'is_seller', False) or request.user.is_superuser):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
