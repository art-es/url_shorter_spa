import logging

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from ..models import ShortenedLink
from ..validators import validate_subpart, validate_url


class ShortenedLinksPaginatedList:
    def __init__(self, query_set, page):
        page_object = Paginator(query_set, settings.OBJECTS_COUNT_IN_PAGE).get_page(
            page
        )

        self.items = [shortened_link.serialize() for shortened_link in page_object]
        self.current_page = page_object.number
        self.total_pages = page_object.paginator.num_pages


class ShortenedLinksService:
    def get_by_page(self, page: int, session_id: str) -> ShortenedLinksPaginatedList:
        query_set = self._get_query_set(session_id)

        return ShortenedLinksPaginatedList(query_set, page)

    def validate(self, original_link, subpart):
        validate_url(original_link)

        if subpart != "":
            validate_subpart(subpart)

            if self._exists(subpart):
                logging.warning(f"subpart {subpart} alredy exists")
                raise SubpartAlreadyExistsException("such subpart alredy exists")

    def create(self, original_link, session_id, subpart=None):
        subpart = subpart or get_random_string(length=settings.SUBPART_LENGTH)

        shortened_link = ShortenedLink(
            original_link=original_link, session_id=session_id, subpart=subpart
        )
        shortened_link.save()

        logging.info(f"create shortened link {shortened_link.get_full_link()}")
        return shortened_link.get_full_link()

    def get_original_link(self, subpart):
        shortened_link = get_object_or_404(ShortenedLink, pk=subpart)

        return shortened_link.original_link

    def _get_query_set(self, session_id: str):
        return ShortenedLink.objects.filter(session_id=session_id).order_by(
            "-created_at"
        )

    def _exists(self, subpart):
        return ShortenedLink.objects.filter(pk=subpart).exists()
