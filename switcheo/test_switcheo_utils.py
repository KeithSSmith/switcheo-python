import unittest
from switcheo.utils import get_epoch_milliseconds, num2hexstring, num2varint, reverse_hex,\
    stringify_message


class TestSwitcheoUtils(unittest.TestCase):

    def test_get_epoch_milliseconds(self):
        self.assertGreaterEqual(get_epoch_milliseconds(), 13)

    def test_num2hexstring(self):
        self.assertEqual(num2hexstring(0), '00')
        self.assertEqual(num2hexstring(255), 'ff')
        self.assertEqual(num2hexstring(256, size=2, little_endian=True), '0001')
        self.assertEqual(num2hexstring(2222, size=2, little_endian=True), 'ae08')

    def test_num2varint(self):
        self.assertEqual(num2varint(0), '00')
        self.assertEqual(num2varint(252), 'fc')
        self.assertEqual(num2varint(253), 'fdfd00')
        self.assertEqual(num2varint(255), 'fdff00')
        self.assertEqual(num2varint(256), 'fd0001')
        self.assertEqual(num2varint(2222), 'fdae08')
        self.assertEqual(num2varint(111111), 'fe07b20100')
        self.assertEqual(num2varint(11111111111), 'ffc719469602000000')

    def test_reverse_hex(self):
        self.assertEqual(reverse_hex('ABCD'), 'CDAB')
        self.assertEqual(reverse_hex('0000000005f5e100'), '00e1f50500000000')

    def test_stringify_message(self):
        json_msg={"name": "John Smith", "age": 27, "siblings": ["Jane", "Joe"]}
        stringify_msg='{"age":27,"name":"John Smith","siblings":["Jane","Joe"]}'
        self.assertEqual(stringify_message(json_msg), stringify_msg)
