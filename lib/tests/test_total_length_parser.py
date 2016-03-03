import unittest
from trait_parsers.total_length_parser import TotalLengthParser


class TestTotalLengthParser(unittest.TestCase):

    def test_1(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"123" };'),
            {'key': 'totalLengthInMM', 'value': '123', 'units': 'MM'})

    def test_2(self):
        self.assertDictEqual(
            target.parse('measurements: ToL=230;TaL=115;HF=22;E=18; total length=230 mm; tail length=115 mm;'),
            {'key': 'total length', 'value': '230', 'units': 'mm'})

    def test_3(self):
        self.assertEqual(
            target.parse('sex=unknown ; crown-rump length=8 mm'),
            None)

    def test_4(self):
        self.assertEqual(
            target.parse('left gonad length=10 mm; right gonad length=10 mm;'),
            None)

    def test_5(self):
        self.assertDictEqual(
            target.parse('"{"measurements":"308-190-45-20" }"'),
            {'key': 'measurements', 'value': '308', 'units': '_mm_'})

    def test_6(self):
        self.assertDictEqual(
            target.parse('308-190-45-20'),
            {'key': '_shorthand_', 'value': '308', 'units': '_mm_'})

    def test_7(self):
        self.assertDictEqual(
            target.parse('{"measurements":"143-63-20-17=13 g" }'),
            {'key': 'measurements', 'value': '143', 'units': '_mm_'})

    def test_8(self):
        self.assertDictEqual(
            target.parse('143-63-20-17=13'),
            {'key': '_shorthand_', 'value': '143', 'units': '_mm_'})

    def test_9(self):
        self.assertDictEqual(
            target.parse('snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g'),
            {'key': 'total length', 'value': '111', 'units': 'mm'})

    def test_10(self):
        self.assertDictEqual(
            target.parse('unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18;'
                         ' total length=230 mm; tail length=115 mm;'),
            {'key': 'total length', 'value': '230', 'units': 'mm'})

    def test_11(self):
        self.assertDictEqual(
            target.parse('** Body length =345 cm; Blubber=1 cm '),
            {'key': 'Body length', 'value': '345', 'units': 'cm'})

    def test_12(self):
        self.assertDictEqual(
            target.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            {'key': 't.l.', 'value': ['2', '3.1 - 4.5'], 'units': ['feet', 'inches']})

    def test_13(self):
        self.assertDictEqual(
            target.parse('2 ft. 3.1 - 4.5 in. '),
            {'key': '_english_', 'value': ['2', '3.1 - 4.5'], 'units': ['ft.', 'in.']})

    def test_14(self):
        self.assertDictEqual(
            target.parse('total length= 2 ft.'),
            {'key': 'total length', 'value': '2', 'units': 'ft.'})

    def test_15(self):
        self.assertDictEqual(
            target.parse('AJR-32   186-102-23-15  15.0g'),
            {'key': '_shorthand_', 'value': '186', 'units': '_mm_'})

    def test_16(self):
        self.assertDictEqual(
            target.parse('length=8 mm'),
            {'key': 'length', 'value': '8', 'units': 'mm'})

    def test_17(self):
        self.assertDictEqual(
            target.parse('another; length=8 mm'),
            {'key': 'length', 'value': '8', 'units': 'mm'})

    def test_18(self):
        self.assertDictEqual(
            target.parse('another; TL_120, noise'),
            {'key': 'TL_', 'value': '120', 'units': None})

    def test_19(self):
        self.assertDictEqual(
            target.parse('another; TL - 101.3mm, noise'),
            {'key': 'TL', 'value': '101.3', 'units': 'mm'})

    def test_20(self):
        self.assertDictEqual(
            target.parse('before; TL153, after'),
            {'key': 'TL', 'value': '153', 'units': None})

    def test_21(self):
        self.assertDictEqual(
            target.parse('before; Total length in catalog and specimen tag as 117, after'),
            {'key': 'Total length', 'value': '117', 'units': None})

    def test_22(self):
        self.assertDictEqual(
            target.parse('before Snout vent lengths range from 16 to 23 mm. after'),
            {'key': 'Snout vent lengths', 'value': '16 to 23', 'units': 'mm.'})

    def test_23(self):
        self.assertDictEqual(
            target.parse('Size=13 cm TL'),
            {'key': 'TL', 'value': '13', 'units': 'cm'})

    def test_24(self):
        self.assertDictEqual(
            target.parse('det_comments:31.5-58.3inTL'),
            {'key': 'TL', 'value': '31.5-58.3', 'units': 'in'})

    def test_25(self):
        self.assertDictEqual(
            target.parse('SVL52mm'),
            {'key': 'SVL', 'value': '52', 'units': 'mm'})

    def test_26(self):
        self.assertDictEqual(
            target.parse('snout-vent length=221 mm; total length=257 mm; tail length=36 mm'),
            {'key': 'total length', 'value': '257', 'units': 'mm'})

    def test_27(self):
        self.assertDictEqual(
            target.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            {'key': 'total', 'value': '272', 'units': 'mm'})

    def test_28(self):
        self.assertDictEqual(
            target.parse('{"time collected":"0712-0900", "length":"12.0" }'),
            {'key': 'length', 'value': '12.0', 'units': None})

    def test_29(self):
        self.assertDictEqual(
            target.parse('{"time collected":"1030", "water depth":"1-8", "bottom":"abrupt lava '
                         'cliff dropping off to sand at 45 ft.", "length":"119-137" }'),
            {'key': 'length', 'value': '119-137', 'units': None})

    def test_30(self):
        self.assertDictEqual(
            target.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            {'key': 'TL', 'value': '44', 'units': 'mm'})

    def test_31(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            {'key': 'totalLengthInMM', 'value': '270', 'units': 'MM'})

    def test_32(self):
        self.assertDictEqual(
            target.parse('{"length":"20-29" }'),
            {'key': 'length', 'value': '20-29', 'units': None})

    def test_33(self):
        self.assertDictEqual(
            target.parse('field measurements on fresh dead specimen were 157-60-20-19-21g'),
            {'key': '_shorthand_', 'value': '157', 'units': '_mm_'})

    def test_34(self):
        self.assertDictEqual(
            target.parse('f age class: adult; standard length: 63-107mm'),
            {'key': 'standard length', 'value': '63-107', 'units': 'mm'})

    def test_35(self):
        self.assertEqual(
            target.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            None)

    def test_36(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18.0-21.5mm'),
            {'key': 'standard length', 'value': '18.0-21.5', 'units': 'mm'})

    def test_37(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18-21.5mm'),
            {'key': 'standard length', 'value': '18-21.5', 'units': 'mm'})

    def test_38(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18.0-21mm'),
            {'key': 'standard length', 'value': '18.0-21', 'units': 'mm'})

    def test_39(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18-21mm'),
            {'key': 'standard length', 'value': '18-21', 'units': 'mm'})

    def test_40(self):
        self.assertEqual(
            target.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                         "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            None)

    def test_41(self):
        self.assertEqual(
            target.parse('20-28mm SL'),
            {'key': 'SL', 'value': '20-28', 'units': 'mm'})

    def test_42(self):
        self.assertEqual(
            target.parse('29mm SL'),
            {'key': 'SL', 'value': '29', 'units': 'mm'})

    def test_43(self):
        self.assertEqual(
            target.parse('{"measurements":"159-?-22-16=21.0" }'),
            {'key': 'measurements', 'value': '159', 'units': '_mm_'})

    def test_44(self):
        self.assertEqual(
            target.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            None)

    def test_45(self):
        self.assertEqual(
            target.parse('Meas: L: 21.0'),
            {'key': 'Meas: L', 'value': '21.0', 'units': '_mm_'})

    def test_46(self):
        self.assertEqual(
            target.parse('Meas: L: 21.0 cm'),
            {'key': 'Meas: L', 'value': '21.0', 'units': 'cm'})

    def test_47(self):
        self.assertEqual(
            target.parse('LABEL. LENGTH 375 MM.'),
            {'key': 'LABEL. LENGTH', 'value': '375', 'units': 'MM.'})

    def test_48(self):
        self.assertEqual(
            target.parse('SL=12mm'),
            {'key': 'SL', 'value': '12', 'units': 'mm'})

    def test_49(self):
        self.assertEqual(
            target.parse('Size=SL 12-14 mm'),
            {'key': 'SL', 'value': '12-14', 'units': 'mm'})

    def test_50(self):
        self.assertEqual(
            target.parse('SV 1.2'),
            {'key': 'SV', 'value': '1.2', 'units': None})

    def test_51(self):
        self.assertEqual(
            target.parse(' Length: 123 mm SL'),
            {'key': 'SL', 'value': '123', 'units': 'mm'})

    def test_52(self):
        self.assertEqual(
            target.parse(' Length: 12-34 mmSL'),
            {'key': 'SL', 'value': '12-34', 'units': 'mm'})

    def test_53(self):
        self.assertEqual(
            target.parse('Measurements: L: 21.0 cm'),
            {'key': 'Measurements: L', 'value': '21.0', 'units': 'cm'})


target = TotalLengthParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTotalLengthParser)
unittest.TextTestRunner().run(suite)
