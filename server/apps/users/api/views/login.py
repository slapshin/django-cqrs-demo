from django.contrib import auth
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.response import Response

from apps.core.api.views import BaseCommandView
from apps.users.logic.commands import login


@extend_schema_serializer(component_name="LoginInput")
class _InputSerializer(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()


class View(BaseCommandView):
    """Login view."""

    command = login.Command
    input_serializer = _InputSerializer

    def create_command(self) -> login.Command:
        """Create command to execute."""
        input_dto = self.extract_input_dto()
        return self.command(
            username=input_dto["username"],
            password=input_dto["password"],
        )

    def build_response(self, command_result: login.CommandResult) -> Response:
        """Build response from command result."""
        auth.login(self.request, command_result.user)
        return super().build_response(command_result)
