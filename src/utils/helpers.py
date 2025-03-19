def validate_input(data):
    """Validates the input data."""
    if not isinstance(data, str) or not data.strip():
        raise ValueError("Input must be a non-empty string.")
    return True

def format_date(date):
    """Formats a date object into a string."""
    if not isinstance(date, datetime.date):
        raise ValueError("Input must be a date object.")
    return date.strftime("%Y-%m-%d")

def calculate_percentage(part, whole):
    """Calculates the percentage of a part from the whole."""
    if whole == 0:
        raise ValueError("Whole must not be zero.")
    return (part / whole) * 100