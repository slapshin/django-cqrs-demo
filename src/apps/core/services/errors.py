import abc

from apps.core.errors import BaseError


class BaseInfrastructureError(BaseError, metaclass=abc.ABCMeta):
    """Base exception for services errors."""
