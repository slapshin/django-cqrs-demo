from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from apps.core.domain.errors import AccessDeniedDomainError
from apps.core.errors import BaseError


class BaseView(View):
    """Base view."""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """Dispatch request."""
        try:
            return super().dispatch(request, *args, **kwargs)
        except BaseError as err:
            return self.handle_error(request, err)

    def handle_error(
        self,
        request: HttpRequest,
        err: BaseError,
    ) -> HttpResponse:
        """Process errors."""
        if isinstance(err, AccessDeniedDomainError):
            return redirect("users:login")

        raise err
