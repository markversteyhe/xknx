import unittest

from xknx.knx import DPT_UElCurrentmA, \
    ConversionError

class TestDPT2byte(unittest.TestCase):
    # pylint: disable=too-many-public-methods,invalid-name

    #
    # DPT_UElCurrentmA
    #
    def test_current_settings(self):
        self.assertEqual(DPT_UElCurrentmA().value_min, 0)
        self.assertEqual(DPT_UElCurrentmA().value_max, 65535)
        self.assertEqual(DPT_UElCurrentmA().unit, "mA")
        self.assertEqual(DPT_UElCurrentmA().resolution, 1)

    def test_current_assert_min_exceeded(self):
        with self.assertRaises(ConversionError):
            DPT_UElCurrentmA().to_knx(-1)

    def test_current_to_knx_exceed_limits(self):
        with self.assertRaises(ConversionError):
            DPT_UElCurrentmA().to_knx(65536)

    def test_current_to_knx_exceed_limits2(self):
        with self.assertRaises(ConversionError):
            DPT_UElCurrentmA().to_knx(-1)

    def test_current_value_max_value(self):
        self.assertEqual(DPT_UElCurrentmA().to_knx(65535), (0xFF, 0xFF))
        self.assertEqual(DPT_UElCurrentmA().from_knx((0xFF, 0xFF)), 65535)

    def test_current_value_min_value(self):
        self.assertEqual(DPT_UElCurrentmA().to_knx(0), (0x00, 0x00))
        self.assertEqual(DPT_UElCurrentmA().from_knx((0x00, 0x00)), 0)

    def test_current_value_38(self):
        self.assertEqual(DPT_UElCurrentmA().to_knx(38), (0x00, 0x26))
        self.assertEqual(DPT_UElCurrentmA().from_knx((0x00, 0x26)), 38)

    def test_current_value_78(self):
        self.assertEqual(DPT_UElCurrentmA().to_knx(78), (0x00, 0x4E))
        self.assertEqual(DPT_UElCurrentmA().from_knx((0x00, 0x4E)), 78)

    def test_current_value_1234(self):
        self.assertEqual(DPT_UElCurrentmA().to_knx(4660), (0x12, 0x34))
        self.assertEqual(DPT_UElCurrentmA().from_knx((0x12, 0x34)), 4660)

    def test_current_wrong_value_from_knx(self):
        with self.assertRaises(ConversionError):
            DPT_UElCurrentmA().from_knx((0xFF, 0x4E, 0x12))

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDPT2byte)
unittest.TextTestRunner(verbosity=2).run(SUITE)