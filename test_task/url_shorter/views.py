import django.contrib.sessions.backends.db
import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import ShortenedLink
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import helper
import redis
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .core.views import base_view
from .core.exceptions import EmptyUrlException
from django.http import JsonResponse
import logging


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, 
                                   db=0)

@require_http_methods(["GET", "POST"])
@base_view
@csrf_exempt
def shortened_links(request):
    """Основной метод. При get-запросе возвращает сслылки для отображения.
    При post-запросе возвращает сокращенную ссылку"""
    if request.method == "GET":
        return get_shortened_links(request)
    else:
        return create_shortened_link(request)


def get_shortened_links(request):
    """Возвращает сокращенные ссылки для отображения в таблице"""
    page_number = request.GET.get('page')

    shorten_links = ShortenedLink.objects.filter(session_id=request.session.session_key).order_by('-created_at')
    paginator = Paginator(shorten_links, 3)
    page_obj = paginator.get_page(page_number)
    serialized_shorten_links = [shorten_link.serialize() for shorten_link in page_obj]

    return JsonResponse({
        'shortened_links': serialized_shorten_links,
        'current_page': page_obj.number,
        'total_pages': page_obj.paginator.num_pages,
    })


def create_shortened_link(request):
    """Создание сокращенной ссылки и ее отправка"""
    if not request.session.session_key:
        request.session.save()

    post_json = json.loads(request.body)
    original_link = post_json.get('original_link')
    subpart = post_json.get('subpart')

    if not original_link:
        logging.warning('URL is empty')
        raise EmptyUrlException("URL is empty")
        
    shortened_link = helper.create_shorten_link(original_link, request.session.session_key, subpart = subpart)
    return JsonResponse(
        {'shortened_link': shortened_link, 'sessionid':request.session.session_key}, 
        headers={'Set-Cookie': f'sessionid={request.session.session_key}'},
    )


@base_view
def redirect_by_short_link(request, subpart):
    """Редирект по сокращенной ссылке"""
    original_link = redis_instance.get(subpart)
    if not original_link:
        shortened_link = get_object_or_404(ShortenedLink, pk=subpart)
        original_link = shortened_link.original_link
        redis_instance.set(subpart, original_link, ex=6000)

    return redirect(original_link)

