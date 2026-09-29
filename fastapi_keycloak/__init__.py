import arrow

try:
    from .settings import get_settings
except ImportError:
    from settings import get_settings

def format_business_date(business_date: arrow.Arrow) -> str:
    return business_date.to("CET").format("DD-MM-YYYY")