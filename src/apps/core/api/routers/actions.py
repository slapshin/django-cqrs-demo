import typing as ty
from collections import defaultdict
from dataclasses import dataclass

from django.urls import path
from django.views import View
from drf_spectacular.utils import extend_schema, extend_schema_serializer
from rest_framework import exceptions, views
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response


@dataclass
class _Route:
    method: str
    handler: ty.Callable[[Request], Response]  # noqa: WPS110


class _ProxyView(views.APIView):  # noqa: WPS338
    routes: list[_Route] | None = None

    @classmethod
    def as_view(cls, **initkwargs) -> View:
        view = super().as_view(**initkwargs)
        view.cls = cls._build_mocked_view_cls(  # noqa: WPS117
            initkwargs["routes"],
        )
        for route in initkwargs["routes"]:
            cls._prepare_route(view, route)

        return view

    @classmethod
    def _prepare_route(cls, view: View, route: _Route):
        func = route.handler
        try:
            schema = func.view_class.get_swagger_schema()  # type: ignore
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
    def _get_scheme_responses(cls, scheme) -> dict[int, str]:
        return {
            status.value: status.phrase
            if response_type is None
            else response_type
            for status, response_type in scheme.responses.items()
        }

    @classmethod
    def _build_mocked_view_cls(cls, routes: list[_Route]) -> type:
        mock_attrs = {}
        mock_base_classes = [views.APIView]
        http_method_names = []
        for route in routes:
            mock_attrs[route.method] = route.handler
            http_method_names.append(route.method)

            view_action = getattr(
                route.handler.view_class,  # type: ignore
                "action",
                "",
            )

            if view_action == "list":
                mock_base_classes.append(ListModelMixin)

        mock_attrs["http_method_names"] = http_method_names  # type: ignore
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

    def _method_not_allowed_response(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
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

    def _get_route_for_request(self, request: Request) -> _Route | None:
        if not self.routes:
            return None

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

    def __init__(self) -> None:
        """Initialize."""
        self._routes_map: dict[str, list[_Route]] = defaultdict(list)

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
