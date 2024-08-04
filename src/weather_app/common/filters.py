import logging
from abc import ABC

from rest_framework.filters import BaseFilterBackend

logger = logging.getLogger(__name__)


class FloatRangeFilter(ABC, BaseFilterBackend):
    """
    Abstract filter class for filtering by range.
    Concrete classes need only to provide the filtering field and the query param.
    """

    field = None
    query_param = None

    def filter_queryset(self, request, queryset, view):
        range_query = request.query_params.get(self.query_param)

        if range_query is None:
            return queryset

        try:
            min_value = float(range_query.strip("[]()").split(",")[0])
            max_value = float(range_query.strip("[]()").split(",")[1])
            if min_value >= max_value:
                raise ValueError(
                    f"Min value must be smaller that max value in {self.field} range."
                )
        except (ValueError, IndexError):
            logger.warning(
                f"Badly formed {self.field} range: {range_query}. "
                f"Two comma-separated values must be provided."
            )
            return queryset.none()

        filter_query = {f"{self.field}__range": (min_value, max_value)}
        return queryset.filter(**filter_query)
