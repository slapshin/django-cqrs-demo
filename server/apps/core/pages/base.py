from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from apps.core.errors import BaseError
from apps.core.logic.errors import (
    ObjectNotFoundError,
    AccessDeniedApplicationError,
)


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
        if isinstance(err, AccessDeniedApplicationError):
            return redirect("users:login")

        raise err
