import unittest
from switcheo.utils import get_epoch_milliseconds, num2hexstring, num2varint, reverse_hex,\
    stringify_message, current_contract_hash, Request
from switcheo.public_client import PublicClient


r = Request(api_url='https://jsonplaceholder.typicode.com/', api_version='')
s = Request()


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
        json_msg = {"name": "John Smith", "age": 27, "siblings": ["Jane", "Joe"]}
        stringify_msg = '{"age":27,"name":"John Smith","siblings":["Jane","Joe"]}'
        self.assertEqual(stringify_message(json_msg), stringify_msg)

    def test_current_contract_hash(self):
        pc = PublicClient()
        expected_current_contract_dict = {
            'NEO': '58efbb3cca7f436a55b1a05c0f36788d2d9a032e',
            'ETH': '0x4d19fd42e780d56ff6464fe9e7d5158aee3d125d',
            'QTUM': 'fake_qtum_contract_hash',
            'EOS': 'toweredbyob2'
        }
        self.assertDictEqual(current_contract_hash(pc.contracts), expected_current_contract_dict)

    def test_request_get(self):
        json_msg = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"}
        self.assertDictEqual(r.get(path='/posts/1'), json_msg)

    def test_request_post(self):
        json_dict = {
            'title': 'foo',
            'body': 'bar',
            'userId': 1}
        json_msg = {
            'id': 101,
            'title': 'foo',
            'body': 'bar',
            'userId': 1}
        self.assertDictEqual(r.post(path='/posts', json_data=json_dict), json_msg)

    def test_request_status(self):
        self.assertDictEqual(s.status(), {'status': 'ok'})
