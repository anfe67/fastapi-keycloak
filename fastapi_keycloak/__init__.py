import arrow


def format_business_date(business_date: arrow.Arrow) -> str:
    return business_date.to("CET").format("DD-MM-YYYY")
