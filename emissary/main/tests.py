from django.test import TestCase

from datetime import datetime, timezone

from emissary.main.models import Link, Visit
from emissary.main.serializers import LinkSerializer, VisitSerializer

class LinkTestCase(TestCase):

    def test_create_basic_link(self):
        link = Link.objects.create(title="Wolverines")
        link.save()

        self.assertEqual("Wolverines", link.title)
        self.assertEqual("wolverines", link.slug)

        # Check that there is less than 5 seconds between now and when it was created
        self.assertTrue((datetime.now(timezone.utc) - link.created_at).total_seconds() < 5)

    def test_complex_autogenerated_slug(self):
        link = Link.objects.create(title="This is a l[ong] slug wíth @ chars.")

        link.save()

        self.assertEqual("this-is-a-l-ong-slug-with-chars", link.slug)


    def test_different_slug(self):
        link = Link.objects.create(title="title 1", slug="completely-unrrelated-slug")
        link.save()

        self.assertEqual("completely-unrrelated-slug", link.slug)

    def test_count_visits(self):
        link = Link.objects.create(title="Link 1")
        link2 = Link.objects.create(title="Link 2")
        link.save()
        link2.save()

        visit1 = Visit.objects.create(link=link)
        visit2 = Visit.objects.create(link=link)
        visit3 = Visit.objects.create(link=link2)
        visit4 = Visit.objects.create(link=link)

        self.assertEqual(3, link.visits_count)
        self.assertEqual(1, link2.visits_count)


class LinkSerializerTestCase(TestCase):

    def test_basic_serialize(self):
        link = Link.objects.create(title="Link 1")
        link.save()

        visit1 = Visit.objects.create(link=link)
        visit2 = Visit.objects.create(link=link)

        serializer = LinkSerializer(link)

        self.assertListEqual(sorted(['created_at', 'slug', 'title', 'visits_count']),
                             sorted(serializer.data.keys()))

