import abc
import types
import typing as ty
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import exceptions, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.docs import SwaggerSchema
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    AuthenticationErrorApplicationError,
    BaseApplicationError,
    InvalidInputApplicationError,
    ObjectNotFoundError,
)

_ERRORS_CODES_MAP = types.MappingProxyType(
    {
        AccessDeniedApplicationError: HTTPStatus.FORBIDDEN,
        AuthenticationErrorApplicationError: HTTPStatus.UNAUTHORIZED,
        (ObjectDoesNotExist, ObjectNotFoundError): HTTPStatus.NOT_FOUND,
        BaseApplicationError: HTTPStatus.BAD_REQUEST,
    },
)


class BaseAPIView(views.APIView, metaclass=abc.ABCMeta):
    """Base api view."""

    swagger_schema: SwaggerSchema
    required_scopes: ty.Tuple[str] = ()

    def initial(self, request: Request, *args, **kwargs):
        """Init request."""
        super().initial(request, *args, **kwargs)

        self.user = None if request.user.is_anonymous else request.user

    def dispatch(self, request: Request, *args, **kwargs) -> HttpResponse:
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

    def handle_request(self, request: Request, *args, **kwargs):
        """Handle request."""
        raise NotImplementedError()

    def get_serializer_context(self):
        """Provides serializer context."""
        return {
            "user": self.user,
        }

    def permission_denied(
        self,
        request: Request,
        message: str | None = None,
        code=None,
    ):
        """Handle permission denied error."""
        is_authenticated = (
            request.authenticators and not request.successful_authenticator
        )  # noqa: WPS332
        if is_authenticated or request.user.is_anonymous:
            raise exceptions.NotAuthenticated()

        raise exceptions.PermissionDenied(detail=message, code=code)

    def handle_exception(self, err: Exception):
        """Handle error."""
        response = None
        if isinstance(err, InvalidInputApplicationError):  # noqa: WPS223
            response = Response(
                data=err.errors,
                status=HTTPStatus.BAD_REQUEST,
            )
        else:
            for error_class, status_code in _ERRORS_CODES_MAP.items():
                if isinstance(err, error_class):
                    response = Response(
                        data={"detail": str(err)},
                        status=status_code,
                    )
                    break

        if response:
            return response

        return super().handle_exception(err)
