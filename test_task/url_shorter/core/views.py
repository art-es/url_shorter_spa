import functools
import logging
import traceback

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .exceptions import EmptyUrlException, SubpartAlreadyExistsException

def error_response(exception, status=500):
    """Отправляется текст ошибки"""
    return JsonResponse(
        {
            "exception": exception.messages
            if hasattr(exception, "messages")
            else str(exception),
        },
        status=status,
    )


def base_view(fn):
    """Декоратор для всех view, обрабатывает исключения"""

    @functools.wraps(fn)
    def inner(requests, *args, **kwargs):
        try:
            return fn(requests, *args, **kwargs)
        except ValidationError as e:
            logging.debug(str(e))
            return error_response(e, 400)
        except Exception as e:
            logging.error(str(e))
            return error_response(e)

    return inner
