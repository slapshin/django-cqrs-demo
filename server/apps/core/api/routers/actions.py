import typing as ty
from collections import defaultdict
from dataclasses import dataclass

from django.urls import path
from drf_spectacular.utils import extend_schema, extend_schema_serializer
from rest_framework import exceptions, views
from rest_framework.mixins import ListModelMixin


@dataclass
class _Route:
    method: str
    handler: ty.Callable  # noqa: WPS110


class _ProxyView(views.APIView):  # noqa: WPS338
    routes = None

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls._build_mocked_view_cls(  # noqa: WPS117
            initkwargs["routes"],
        )
        for route in initkwargs["routes"]:
            cls._prepare_route(view, route)

        return view

    @classmethod
    def _prepare_route(cls, view, route):
        try:
            schema = route.handler.view_class.get_swagger_schema()
        except AttributeError:
            return

        extend_schema(
            methods=[route.method],
            responses=cls._get_scheme_responses(schema),
            parameters=[
                extend_schema_serializer()(
                    schema.query_serializer,
                ),
            ],
            request=schema.request_body,
            description=schema.operation_description,
            summary=schema.operation_summary,
        )(view)

    @classmethod
    def _get_scheme_responses(cls, scheme):
        return {
            status.value: status.phrase
            if response_type is None
            else response_type
            for status, response_type in scheme.responses.items()
        }

    @classmethod
    def _build_mocked_view_cls(cls, routes):
        mock_attrs = {}
        mock_base_classes = [views.APIView]
        http_method_names = []
        for route in routes:
            mock_attrs[route.method] = route.handler
            http_method_names.append(route.method)
            if getattr(route.handler.view_class, "action", "") == "list":
                mock_base_classes.append(ListModelMixin)

        mock_attrs["http_method_names"] = http_method_names
        return type(
            "MockedApiView",
            tuple(mock_base_classes),
            mock_attrs,
        )

    def dispatch(self, request, *args, **kwargs):
        route = self._get_route_for_request(request)
        if route:
            return route.handler(request, *args, **kwargs)

        return self._method_not_allowed_response(request, *args, **kwargs)

    def _method_not_allowed_response(self, request, *args, **kwargs):
        response = self.handle_exception(
            exceptions.MethodNotAllowed(request.method),
        )
        self.headers = self.default_response_headers
        self.response = self.finalize_response(
            request,
            response,
            *args,
            **kwargs,
        )
        return self.response

    def _get_route_for_request(self, request):
        return next(
            (
                route
                for route in self.routes
                if route.method == request.method.lower()
            ),
            None,
        )


class ActionsRouter:
    """Action router description."""

    def __init__(self):
        """Initialize."""
        self._routes_map = defaultdict(list)

    def delete(self, pattern, handler):  # noqa: WPS110
        """Registers DELETE api request."""
        self._routes_map[pattern].append(_Route("delete", handler))

    @property
    def urls(self) -> list[path]:
        """Return list of registered urls."""
        return [
            path(pattern, _ProxyView.as_view(routes=routes))
            for pattern, routes in self._routes_map.items()
        ]

    def post(self, pattern, handler):  # noqa: WPS110
        """Registers POST api request."""
        self._routes_map[pattern].append(_Route("post", handler))

    def put(self, pattern, handler):  # noqa: WPS110
        """Registers PUT api request."""
        self._routes_map[pattern].append(_Route("put", handler))

    def get(self, pattern, handler):  # noqa: WPS110
        """Registers GET api request."""
        self._routes_map[pattern].append(_Route("get", handler))

    def patch(self, pattern, handler):  # noqa: WPS110
        """Registers PATCH api request."""
        self._routes_map[pattern].append(_Route("patch", handler))
