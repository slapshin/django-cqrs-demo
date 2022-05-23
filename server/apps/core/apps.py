from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _

from apps.core import injector


class AppConfig(BaseAppConfig):
    """Application "core" config."""

    name = "apps.core"
    default = True
    verbose_name = _("VN__CORE")

    def ready(self):
        """App ready callback."""
        super().ready()

        self._setup_dependency_injection()

    def _setup_dependency_injection(self) -> None:
        from apps.core.logic.modules import (  # noqa: WPS433
            CoreApplicationModule,
        )
        from apps.core.services.modules import (  # noqa: WPS433
            CodeInfrastructureModule,
        )

        injector.binder.install(CoreApplicationModule)
        injector.binder.install(CodeInfrastructureModule)
