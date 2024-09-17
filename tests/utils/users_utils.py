import datetime


def string_to_datetime(string: str) -> datetime.datetime:
    dt = datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=datetime.timezone.utc)
