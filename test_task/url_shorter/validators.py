import logging

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_subpart(subpart: str):
    logging.debug(f"validate subpart:{subpart}")
    validators.RegexValidator(
        r"^[A-Za-z0-9]*$",
        "Only numbers and letters are allowed",
    )(subpart)
    if len(subpart) > settings.SUBPART_LENGTH:
        raise ValidationError(f"Allowed only in lengths of {settings.SUBPART_LENGTH}")


def validate_url(url: str):
    logging.debug(f"validate url: \"{url}\"")
    validator = URLValidator()
    return validator(url)
