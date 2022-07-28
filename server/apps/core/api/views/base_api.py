import abc
import types
import typing as ty
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.docs import SwaggerSchema
from apps.core.domain.errors import (
    AccessDeniedDomainError,
    AuthenticationDomainError,
    BaseDomainError,
    ObjectNotFoundDomainError,
    ValidationDomainError,
)

_ERRORS_CODES_MAP = types.MappingProxyType(
    {
        AccessDeniedDomainError: HTTPStatus.FORBIDDEN,
        AuthenticationDomainError: HTTPStatus.UNAUTHORIZED,
        (
            ObjectDoesNotExist,
            ObjectNotFoundDomainError,
        ): HTTPStatus.NOT_FOUND,
        BaseDomainError: HTTPStatus.BAD_REQUEST,
    },
)


class BaseAPIView(views.APIView, metaclass=abc.ABCMeta):
    """Base api view."""

    swagger_schema: SwaggerSchema

    def initial(self, request: Request, *args, **kwargs):
        """Init request."""
        super().initial(request, *args, **kwargs)

        self.user = None if request.user.is_anonymous else request.user

    def dispatch(self, request: Request, *args, **kwargs) -> Response:
        """Dispatch request."""
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        self.initial(request, *args, **kwargs)
        try:
            response = self.handle_request(request, *args, **kwargs)
        except Exception as err:
            response = self.handle_exception(err)

        self.response = self.finalize_response(
            request,
            response,
            *args,
            **kwargs,
        )
        return self.response

    def handle_request(self, request: Request, *args, **kwargs) -> Response:
        """Handle request."""
        raise NotImplementedError()

    def get_serializer_context(self) -> dict[str, ty.Any]:
        """Provides serializer context."""
        return {
            "user": self.user,
        }

    def handle_exception(self, err: Exception) -> Response:
        """Handle error."""
        response = None
        if isinstance(err, ValidationDomainError):  # noqa: WPS223
            response = Response(
                data=err.errors,
                status=HTTPStatus.BAD_REQUEST,
            )
        else:
            for error_class, status_code in _ERRORS_CODES_MAP.items():
                if isinstance(err, error_class):
                    response = Response(
                        data={"detail": str(err.message)},
                        status=status_code,
                    )
                    break

        if response:
            return response

        return super().handle_exception(err)
