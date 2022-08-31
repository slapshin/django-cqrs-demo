from django.contrib import auth
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.response import Response

from apps.core.api.views import BaseCommandView
from apps.users.logic.commands import register


@extend_schema_serializer(component_name="RegisterInput")
class _InputSerializer(serializers.Serializer):
    email = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class View(BaseCommandView):
    """Register view."""

    command = register.Command
    input_serializer = _InputSerializer

    def create_command(self) -> register.Command:
        """Create command to execute."""
        input_dto = self.extract_input_dto()
        return self.command(
            email=input_dto["email"],
            password1=input_dto["password1"],
            password2=input_dto["password2"],
        )

    def build_response(
        self,
        command_result: register.CommandResult,
    ) -> Response:
        """Build response from command result."""
        auth.login(self.request, command_result.user)
        return super().build_response(command_result)
