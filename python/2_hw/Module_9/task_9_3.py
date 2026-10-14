"""Tell which season a month belongs to."""

WINTER_MONTHS = ("December", "January", "February")
SPRING_MONTHS = ("March", "April", "May")
SUMMER_MONTHS = ("June", "July", "August")
AUTUMN_MONTHS = ("September", "October", "November")


def check_season(month):
    """Return the season the given month belongs to.

    Args:
        month: Name of the month, for example "January".

    Returns:
        The season name, or None if the month name is not recognised.
    """
    if month in WINTER_MONTHS:
        return "Winter"

    if month in SPRING_MONTHS:
        return "Spring"

    if month in SUMMER_MONTHS:
        return "Summer"

    if month in AUTUMN_MONTHS:
        return "Autumn"

    return None


print(check_season("January"))
print(check_season("April"))
print(check_season("July"))
print(check_season("October"))
print(check_season("Octobr"))
