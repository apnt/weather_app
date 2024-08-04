from datetime import datetime
from uuid import UUID

from weather_app.common.constants import VALID_DATE_INPUT_FORMATS


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def convert_str_to_datetime(datetime_str):
    for date_format in VALID_DATE_INPUT_FORMATS:
        try:
            return datetime.strptime(datetime_str, date_format)
        except ValueError:
            pass
