import unittest
from switcheo.Fixed8 import SwitcheoFixed8, num2fixed8


class TestFixed8(unittest.TestCase):

    def test_fixed8_inheritance(self):
        self.assertEqual(SwitcheoFixed8(2050000).ToString(), '0.0205')
        self.assertEqual(SwitcheoFixed8(100000000).ToInt(), 1)

    def test_to_hex(self):
        self.assertEqual(SwitcheoFixed8(205).toHex(), '00000004c5e52d00')
        self.assertEqual(SwitcheoFixed8(0.0205).toHex(), '00000000001f47d0')

    def test_to_reverse_hex(self):
        self.assertEqual(SwitcheoFixed8(205).toReverseHex(), '002de5c504000000')
        self.assertEqual(SwitcheoFixed8(0.0205).toReverseHex(), 'd0471f0000000000')

    def test_num2fixed8(self):
        self.assertEqual(num2fixed8(205), '002de5c504000000')
        self.assertEqual(num2fixed8(0.0205), 'd0471f0000000000')
        with self.assertRaises(ValueError):
            num2fixed8(205, size=1.1)
