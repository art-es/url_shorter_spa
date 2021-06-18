import functools
import traceback
from django.shortcuts import redirect, reverse
from .exceptions import EmptyUrlException, SubpartAlreadyExistsException
from django.http import JsonResponse


def error_response(exception, status=500):
    """Отправляется текст ошибки"""
    return JsonResponse({
        'exception': str(exception),
    }, status=status)

def base_view(fn):
    """Декоратор для всех view, обрабатывает исключения"""
    @functools.wraps(fn)
    def inner(requests, *args, **kwargs):
        try:
            return fn(requests, *args, **kwargs)
        except (EmptyUrlException, SubpartAlreadyExistsException) as e:
            return error_response(e, 400)
        except Exception as e:
            logging.error(str(e))
            return error_response(e)
    return inner