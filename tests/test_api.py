#!/usr/bin/env python
import pyzbx
import unittest
import httpretty
import json


class TestPyzbx(unittest.TestCase):
    '''pyzbx test class. '''

    @httpretty.activate
    def test_getAuthCode(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://zabbix_server[:port]/zabbix/api_jsonrpc.php",
            body=json.dumps({
                "jsonrpc": "2.0",
                "result": "693df78d1bad9a7b335b640846c56ccf",
                'id': 0
            }),
        )
        zapi = pyzbx.ZbxAPI(
            zabbix_url="http://zabbix_server[:port]/zabbix/api_jsonrpc.php",
            user="user",
            password="password")

        # check response
        self.assertEqual(
            zapi.getAuthCode(),
            "693df78d1bad9a7b335b640846c56ccf")

if __name__ == "__main__":
    unittest.main()
