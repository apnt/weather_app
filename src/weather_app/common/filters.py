import logging
from abc import ABC, abstractmethod

from rest_framework.filters import BaseFilterBackend

from weather_app.common.utils import convert_str_to_datetime

logger = logging.getLogger(__name__)


class RangeFilter(ABC, BaseFilterBackend):
    """Abstract filter class for filtering by range."""

    field = None
    query_param = None

    @abstractmethod
    def parse_query_values(self, query):
        """Implement parsing of the query param value."""

    def filter_queryset(self, request, queryset, view):
        range_query = request.query_params.get(self.query_param)

        if range_query is None:
            return queryset

        try:
            min_value, max_value = self.parse_query_values(range_query)

            if min_value > max_value:
                logger.warning(
                    f"Min value must be smaller that max value in {self.field} range."
                )
                return queryset.none()
        except (ValueError, IndexError):
            logger.warning(
                f"Badly formed {self.field} range: {range_query}. "
                f"Two comma-separated values must be provided."
            )
            return queryset.none()

        filter_query = {f"{self.field}__range": (min_value, max_value)}
        return queryset.filter(**filter_query)


class FloatRangeFilter(RangeFilter):
    """
    Generic filter class for filtering by float range.
    Specific classes need only to provide the filtering field and the query param.
    """

    def parse_query_values(self, query):
        min_value = float(query.strip("[]()").split(",")[0])
        max_value = float(query.strip("[]()").split(",")[1])
        return min_value, max_value


class DateRangeFilter(RangeFilter):
    """
    Generic filter class for filtering date by range.
    Specific classes need only to provide the filtering field and the query param.
    """

    def parse_query_values(self, query):
        start_date = convert_str_to_datetime(query.strip("[]()").split(",")[0])
        end_date = convert_str_to_datetime(query.strip("[]()").split(",")[0])
        return start_date, end_date


class SingleValueFilter(ABC, BaseFilterBackend):
    """Abstract filter class for filtering by given value."""

    gte = None
    field = None
    query_param = None

    @abstractmethod
    def parse_query_value(self, query):
        """Implement parsing of the query param value."""

    def filter_queryset(self, request, queryset, view):
        query = request.query_params.get(self.query_param)

        if query is None:
            return queryset

        try:
            value = self.parse_query_value(query)
        except (ValueError, IndexError):
            logger.warning(f"Badly formed {self.field} query: {query}. ")
            return queryset.none()

        filter_query = (
            {f"{self.field}__gte": query} if self.gte else {f"{self.field}__lte": query}
        )
        return queryset.filter(**filter_query)


class SingleFloatFilter(SingleValueFilter):
    """
    Generic filter class for filtering by a single float value.
    Specific classes need only to provide the comparison
    (greater/smaller), the filtering field and the query param.
    """

    def parse_query_value(self, query):
        return float(query)


class SingleDateFilter(SingleValueFilter):
    """
    Generic filter class for filtering by a single date.
    Specific classes need only to provide the comparison
    (greater/smaller), the filtering field and the query param.
    """

    def parse_query_value(self, query):
        return convert_str_to_datetime(query)
