import abc

from apps.core.errors import BaseError


class BaseApplicationError(BaseError, metaclass=abc.ABCMeta):
    """Base exception for services errors."""
