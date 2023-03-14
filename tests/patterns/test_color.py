import unittest

from tests.setup import test


class TestColor(unittest.TestCase):
    def test_color_01(self):
        self.assertEqual(
            test(
                """hypanthium green or greenish yellow,
                usually not purple-spotted, rarely purple-spotted distally.
                """
            ),
            [
                {
                    "color": "green",
                    "trait": "color",
                    "start": 11,
                    "end": 16,
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "start": 20,
                    "end": 35,
                },
                {
                    "color": "purple-spotted",
                    "missing": True,
                    "trait": "color",
                    "start": 45,
                    "end": 63,
                },
                {
                    "color": "purple-spotted",
                    "missing": True,
                    "trait": "color",
                    "start": 65,
                    "end": 86,
                },
            ],
        )

    def test_color_02(self):
        self.assertEqual(
            test("hypanthium straw-colored to sulphur-yellow or golden-yellow."),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 11,
                    "end": 24,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 28,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 46,
                    "end": 59,
                },
            ],
        )

    def test_color_03(self):
        self.assertEqual(
            test("sepals erect, green- or red-tipped."),
            [
                {
                    "color": "green",
                    "trait": "color",
                    "start": 14,
                    "end": 20,
                },
                {
                    "color": "red-tipped",
                    "trait": "color",
                    "start": 24,
                    "end": 34,
                },
            ],
        )

    def test_color_04(self):
        self.assertEqual(
            test("petals white, cream, or pale green [orange to yellow]."),
            [
                {
                    "color": "white",
                    "trait": "color",
                    "start": 7,
                    "end": 12,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "start": 14,
                    "end": 19,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "start": 24,
                    "end": 34,
                },
                {
                    "color": "orange",
                    "trait": "color",
                    "start": 36,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 46,
                    "end": 52,
                },
            ],
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                petals distinct, white to cream, greenish yellow,
                maturing yellowish or pale brown, commonly mottled or with
                light green or white longitudinal stripes.
                """
            ),
            [
                {
                    "color": "white",
                    "trait": "color",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "start": 33,
                    "end": 48,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 59,
                    "end": 68,
                },
                {
                    "color": "brown",
                    "trait": "color",
                    "start": 72,
                    "end": 82,
                },
                {"color_mod": "mottled", "end": 100, "start": 93, "trait": "color_mod"},
                {
                    "color": "green",
                    "trait": "color",
                    "start": 109,
                    "end": 120,
                },
                {
                    "color": "white-longitudinal-stripes",
                    "trait": "color",
                    "start": 124,
                    "end": 150,
                },
            ],
        )

    def test_color_06(self):
        self.assertEqual(
            test(
                """
                Petals distinct, white to cream, greenish white,
                or yellowish green, or yellowish, usually green-throated
                and faintly green-lined.
                """
            ),
            [
                {
                    "color": "white",
                    "trait": "color",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-white",
                    "trait": "color",
                    "start": 33,
                    "end": 47,
                },
                {
                    "color": "yellow-green",
                    "trait": "color",
                    "start": 52,
                    "end": 67,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 72,
                    "end": 81,
                },
                {
                    "color": "green-throated",
                    "trait": "color",
                    "start": 91,
                    "end": 105,
                },
                {
                    "color": "green-lined",
                    "trait": "color",
                    "start": 110,
                    "end": 129,
                },
            ],
        )

    def test_color_07(self):
        self.assertEqual(
            test("calyx yellow"),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_08(self):
        self.assertEqual(
            test("corolla yellow"),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 8,
                    "end": 14,
                },
            ],
        )

    def test_color_09(self):
        self.assertEqual(
            test("flower yellow"),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 7,
                    "end": 13,
                },
            ],
        )

    def test_color_10(self):
        self.assertEqual(
            test("hypanthium yellow"),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 11,
                    "end": 17,
                },
            ],
        )

    def test_color_11(self):
        self.assertEqual(
            test("petal pale sulfur-yellow."),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 6,
                    "end": 24,
                },
            ],
        )

    def test_color_12(self):
        self.assertEqual(
            test("sepal yellow"),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_13(self):
        self.assertEqual(
            test("Leaves acaulescent or nearly so, with white hairs."),
            [
                {
                    "color": "white",
                    "trait": "color",
                    "start": 38,
                    "end": 43,
                },
            ],
        )

    def test_color_14(self):
        self.assertEqual(
            test("leaflets surfaces rather densely spotted with blackish dots"),
            [
                {"color_mod": "spotted", "end": 40, "start": 33, "trait": "color_mod"},
                {
                    "color": "black-dots",
                    "trait": "color",
                    "start": 46,
                    "end": 59,
                },
            ],
        )

    def test_color_15(self):
        self.assertEqual(
            test("Petals purplish in life, whitish yellowish when dry;"),
            [
                {
                    "color": "purple",
                    "trait": "color",
                    "start": 7,
                    "end": 15,
                },
                {
                    "color": "white-yellow",
                    "trait": "color",
                    "start": 25,
                    "end": 42,
                },
            ],
        )

    def test_color_16(self):
        self.assertEqual(
            test("Petals red or golden yellowish"),
            [
                {
                    "color": "red",
                    "trait": "color",
                    "start": 7,
                    "end": 10,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 14,
                    "end": 30,
                },
            ],
        )

    def test_color_17(self):
        self.assertEqual(
            test("twigs: young growth green or reddish-tinged."),
            [
                {
                    "color": "green",
                    "trait": "color",
                    "start": 20,
                    "end": 25,
                },
                {
                    "color": "red-tinged",
                    "trait": "color",
                    "start": 29,
                    "end": 43,
                },
            ],
        )

    def test_color_18(self):
        self.assertEqual(
            test(
                """stipules, the young stems and lf-axes hispid with stout, partly
                confluent or branched, yellowish setae"""
            ),
            [
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 87,
                    "end": 96,
                },
            ],
        )
