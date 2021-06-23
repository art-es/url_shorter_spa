import json

import redis
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .core.services import ShortenedLinksService
from .core.views import base_view

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)
shortened_links_service = ShortenedLinksService()


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
    page_number = request.GET.get("page")
    session_id = request.session.session_key

    paginated = shortened_links_service.get_by_page(page_number, session_id)

    return JsonResponse(
        {
            "shortened_links": paginated.items,
            "current_page": paginated.current_page,
            "total_pages": paginated.total_pages,
        }
    )


def create_shortened_link(request):
    """Создание сокращенной ссылки и ее отправка"""
    if not request.session.session_key:
        request.session.save()

    post_json = json.loads(request.body)
    original_link = post_json.get("original_link")
    subpart = post_json.get("subpart")
    session_id = request.session.session_key

    shortened_links_service.validate(original_link, subpart)
    shortened_link = shortened_links_service.create(original_link, session_id, subpart)

    return JsonResponse(
        {"shortened_link": shortened_link, "sessionid": request.session.session_key},
        headers={"Set-Cookie": f"sessionid={request.session.session_key}"},
    )


@base_view
def redirect_by_short_link(request, subpart):
    """Редирект по сокращенной ссылке"""
    cached_original_link = redis_instance.get(subpart)
    if cached_original_link:
        return redirect(cached_original_link.decode())

    original_link = shortened_links_service.get_original_link(subpart)
    redis_instance.set(subpart, original_link)

    return redirect(original_link)
