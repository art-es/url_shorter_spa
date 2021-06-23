from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase
from django.utils.crypto import get_random_string

from ..models import ShortenedLink
from .services import ShortenedLinksService

shortened_links_service = ShortenedLinksService()


class TestsShortenedLinksService(TransactionTestCase):
    reset_sequences = True
    cleans_up_after_itself = True
    test_session = get_random_string(32)

    def test_get_by_page(self):
        # one element
        ShortenedLink.objects.bulk_create(
            [
                ShortenedLink(
                    original_link="http://example.com",
                    session_id=self.test_session,
                    subpart=get_random_string(5),
                ),
            ]
        )
        pages = shortened_links_service.get_by_page(1, self.test_session)
        self.assertEqual(len(pages.items), 1)
        self.assertEqual(pages.current_page, 1)
        self.assertEqual(pages.total_pages, 1)

        # full list
        ShortenedLink.objects.bulk_create(
            [
                ShortenedLink(
                    original_link="http://example.com",
                    session_id=self.test_session,
                    subpart=get_random_string(5),
                ),
                ShortenedLink(
                    original_link="http://example.com",
                    session_id=self.test_session,
                    subpart=get_random_string(5),
                ),
            ]
        )
        pages = shortened_links_service.get_by_page(1, self.test_session)
        self.assertEqual(len(pages.items), 3)
        self.assertEqual(pages.current_page, 1)
        self.assertEqual(pages.total_pages, 1)

        # page < 0
        pages = shortened_links_service.get_by_page(1, self.test_session)
        self.assertEqual(len(pages.items), 3)
        self.assertEqual(pages.current_page, 1)
        self.assertEqual(pages.total_pages, 1)

        # page > total_pages
        ShortenedLink.objects.bulk_create(
            [
                ShortenedLink(
                    original_link="http://example.com",
                    session_id=self.test_session,
                    subpart=get_random_string(5),
                ),
            ]
        )
        pages = shortened_links_service.get_by_page(3, self.test_session)
        self.assertEqual(len(pages.items), 1)
        self.assertEqual(pages.current_page, 2)
        self.assertEqual(pages.total_pages, 2)

    def test_create(self):
        ShortenedLink.objects.all().delete()

        # empty subpart
        full_link = shortened_links_service.create(
            "http://example.com", self.test_session, ""
        )
        self.assertEqual(ShortenedLink.objects.all().count(), 1)
        self.assertNotEqual(ShortenedLink.objects.get().subpart, "")
        self.assertNotEqual(full_link, "")

        # non-empty subpart
        test_subpart = "qwe12"
        full_link = shortened_links_service.create(
            "http://example.com", self.test_session, test_subpart
        )
        self.assertEqual(ShortenedLink.objects.all().count(), 2)
        self.assertEqual(ShortenedLink.objects.filter(pk=test_subpart).exists(), True)
        self.assertEqual(full_link, f"http://localhost:8000/{test_subpart}")

        # busy subpart
        shortened_links_service.create(
            "http://example.com/2", self.test_session, test_subpart
        )
        self.assertEqual(ShortenedLink.objects.all().count(), 2)
        self.assertEqual(
            ShortenedLink.objects.filter(pk=test_subpart).get().original_link,
            "http://example.com/2",
        )

        # empty original_link
        full_link = shortened_links_service.create("", self.test_session, "")
        self.assertEqual(ShortenedLink.objects.all().count(), 3)
        self.assertEqual(
            ShortenedLink.objects.order_by("-created_at")[0].original_link, ""
        )

    def test_validate(self):
        # invalid original_link
        try:
            shortened_links_service.validate("invalid_original_link", "")
        except ValidationError as e:
            self.assertEqual(e.messages[0], "Enter a valid URL.")

        # empty original_link
        try:
            shortened_links_service.validate("", "")
        except ValidationError as e:
            self.assertEqual(e.messages[0], "Enter a valid URL.")

        # invalid subpart (used incorrect chars)
        try:
            shortened_links_service.validate("http://example.com", "%qwe1")
        except ValidationError as e:
            self.assertEqual(e.messages[0], "Only numbers and letters are allowed")

        # invalid subpart (too long subpart)
        try:
            shortened_links_service.validate(
                "http://example.com", get_random_string(settings.SUBPART_LENGTH + 1)
            )
        except ValidationError as e:
            self.assertEqual(
                e.messages[0], f"Allowed only in lengths of {settings.SUBPART_LENGTH}"
            )

        # empty subpart
        shortened_links_service.validate("http://example.com", "")
