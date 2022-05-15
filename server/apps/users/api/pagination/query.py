from django.core.paginator import InvalidPage
from django.utils.translation import gettext_lazy as _


class ListPagination:
    """List pagination."""

    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100
    page_size = 20

    @classmethod
    def get_page_number(cls, input_dto) -> int:  # noqa: WPS615
        """Get page number."""
        return cls._positive_int(
            input_dto.get(cls.page_query_param, 1),
        )

    @classmethod
    def get_page_size(cls, input_dto) -> int:  # noqa: WPS615
        """Get page size."""
        page_size = input_dto.get(cls.page_size_query_param, cls.page_size)

        return cls._positive_int(
            page_size,
            strict=True,
            cutoff=cls.max_page_size,
        )

    @classmethod
    def _positive_int(
        cls,
        int_value: int,
        strict: bool = False,
        cutoff: int | None = None,
    ) -> int:
        if int_value < 0 or (int_value == 0 and strict):
            raise InvalidPage(_("Page number is negative or zero."))
        if cutoff:
            return min(int_value, cutoff)
        return int_value
