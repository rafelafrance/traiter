import unittest

from tests.setup import parse
from traiter.pylib.rules.date_ import Date
from traiter.pylib.rules.uuid import Uuid


class TestUuid(unittest.TestCase):
    def test_uuid_01(self):
        self.assertEqual(
            parse("c701563b-dbd9-4500-184f-1ad61eb8da11"),
            [
                Uuid(
                    uuid="c701563b-dbd9-4500-184f-1ad61eb8da11",
                    trait="uuid",
                    start=0,
                    end=36,
                ),
            ],
        )

    def test_uuid_02(self):
        self.assertEqual(
            parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'
            ),
            [
                Date(
                    trait="date",
                    start=13,
                    end=23,
                    date="2014-10-29",
                ),
                Uuid(
                    uuid="eeba8b10-040e-4477-a0a6-870102b56234",
                    trait="uuid",
                    start=48,
                    end=84,
                ),
                Uuid(
                    uuid="abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86",
                    trait="uuid",
                    start=85,
                    end=121,
                ),
            ],
        )
