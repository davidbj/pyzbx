#!/usr/bin/env python
#import sys
#import os
#pyzbx = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(pyzbx)
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
                "http://zabbix.chunbo.com/zabbix/api_jsonrpc.php",
                body=json.dumps({
                    "jsonrpc": "2.0",
                    "result": "693df78d1bad9a7b335b640846c56ccf",
                    'id': 0
                }),
        )
        zapi = pyzbx.ZbxAPI(zabbix_url="http://zabbix.chunbo.com/zabbix/api_jsonrpc.php", user="admin", password="Chunb0@2o14")

        #check response
        self.assertEqual(zapi.getAuthCode(), "693df78d1bad9a7b335b640846c56ccf")

if __name__ == "__main__":
    unittest.main()
