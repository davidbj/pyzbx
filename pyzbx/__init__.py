__Author__ = 'shaozhi.zhang<davidbjhd@gmail.com>'

import json
import urllib2 

class ZbxAPI(object):
    def __init__(self,
                 zabbix_url = 'http://localhost/zabbix',
                 user = '',
                 password = ''):
        '''
        Parameters:
            zabbix_url: Base URI for zabbix web interface.
            user: Sign zabbix username.
            password: Sign zabbix password.
        '''
        self.zabbix_url = zabbix_url
        self.user = user
        self.password = password
        self.header = {"Content-Type":"application/json"}

    def do_request(self, method, params=None, id=0, auth=False):
        if not auth:
            request_json = json.dumps({
                'jsonrpc': '2.0',
                'method': method,
                'params': params or {},
                'id': id,
            })
        else:
            request_json = json.dumps({
                'jsonrpc': '2.0',
                'method': method,
                'params': params or {},
                'auth': auth,
                'id': id,
            })
        return request_json

    def getAuthCode(self):
        '''get zabbix auth code.'''
        request_json = self.do_request('user.login', params = {'user': self.user, 'password': self.password})
        request = urllib2.Request(self.zabbix_url, request_json)
        for key in self.header:
            request.add_header(key, self.header.get(key))

        try:
            result = urllib2.urlopen(request)
        except Exception  as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()
        if response:
            return response.get('result')

    def getHostid(self, monitor_hostname=''):
        '''get monitor host hostid.
        parameters:
            monitor_hostname: zabbix item hostname.
        '''
        request_json = self.do_request('host.get', params = {'output': 'extend', 'filter': {'host': monitor_hostname}}, id=1, auth=self.getAuthCode())
        request = urllib2.Request(self.zabbix_url, request_json)
        for key in self.header:
            request.add_header(key, self.header.get(key))

        try:
            result = urllib2.urlopen(request)
        except Exception  as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()
        hostid = response.get('result')[0].get('hostid')
        return hostid

    def getItemid(self, monitor_item_key=''):
        '''get monitor host itemid.
        parameters:
            monitor_item_key: zabbix monitoring key value.

            result zabbix item's itemid.
        '''
        request_json = self.do_request('item.get', 
                                       params={
                                                'output': 'extend', 
                                                'hostids': self.getHostid(), 
                                                'search': {'_Key': monitor_item_key},
                                                'sortfield': 'name'
                                                },
                                       auth=self.getAuthCode(),
                                       id=1)

        request = urllib2.Request(self.zabbix_url, request_json)
        for key in self.header:
            request.add_header(key, self.header.get(key))

        try:
            result = urllib2.urlopen(request)
        except Exception  as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()

        try:
            itemid = response['result'][0]['itemid']
        except LookupError as e:
            print '''No results are returned. If the auto-discovery monitoring item, use the "key_" field search. For example:   
            response = GetItemid(zabbix_url, zabbix_login_username, zabbix_login_passwd, monitor_hostname, "Free disk space on /data")
            response.getItemid()
            ''' 
            exit(1)
        return itemid

    def getHistoryData(self, monitor_item_key='', **kwargs):
        '''git zabbix history data.
        Parameters:
            monitor_item_key: zabbix monitoring key value.
            kwargs: Referring to the specific parameters https://www.zabbix.com/documentation/1.8/api/history/get.

            example:
                response = ZbxAPI(zabbix_url='http://localhost/zabbix/api_jsonrpc.php', user="", password='')
                response.getHistoryData(monitor_item_key='system.cpu.util[,steal]', history=3, output='extend', limit=10)
        '''
        itemid = self.getItemid(monitor_item_key=monitor_item_key)
        params = {}
        for k, v in kwargs.iteritems():
            params[k] = v
        params.setdefault('itemids',itemid.encode('ascii'))
        
        request_json = self.do_request('history.get',
                                       params=params,
                                       auth=self.getAuthCode(),
                                       id=2)
        request = urllib2.Request(self.zabbix_url, request_json)
        for key in self.header:
            request.add_header(key, self.header.get(key))
        try:
            result = urllib2.urlopen(request)
        except Exception as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()
        return response
