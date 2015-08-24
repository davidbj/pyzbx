__Author__ = 'shaozhi.zhang<davidbjhd@gmail.com>'

import json
import urllib2 

class GetItemid(object):
    def __init__(self,zabbix_url, user, passwd, monitor_hostname, monitor_item_key):
        self.zabbix_url = zabbix_url
        self.user = user
        self.passwd = passwd
        self.monitor_hostname = monitor_hostname
        self.monitor_item_key  = monitor_item_key
        self.postData = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.passwd
            },
            "id": 0
        })
        self.header = {"Content-Type":"application/json"}

    @classmethod
    def getAuthCode(self):
        request = urllib2.Request(self.zabbix_url, self.postData)
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
            return response['result']

    def getHostid(self):
        '''get monitor host hostid.'''

        posthostidData = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": self.monitor_hostname,
                }
            },
            "auth": self.getAuthCode(),
            "id": 1
        })

        request = urllib2.Request(self.zabbix_url, posthostidData)
        for key in self.header:
            request.add_header(key, self.header.get(key))

        try:
            result = urllib2.urlopen(request)
        except Exception  as e:
            print "Auth Failed, Please Check Your Name AndPassword:", e.code
        else:
            response = json.loads(result.read())
            result.close()
        hostid = response['result'][0].get('hostid')
        return hostid

    def getItemid(self):
        '''get monitor host itemid.'''
        postitemidData = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": self.getHostid(),
                "search": {
                    '_key': self.monitor_item_key 
                },
                "sortfield": "name"
            },
            "auth": self.getAuthCode(),
            "id": 1
        })

        request = urllib2.Request(self.zabbix_url, postitemidData)
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


class GetRawdata(object):
    def __init__(self, itemid):
        self.itemid = self.itemid
        self.auth = GetItemid.getAuthCode()

    def getHistoryData(self):
        '''get zabbix history data api.'''
        pass


if __name__ == "__main__":
    c = GetItemid('http://zabbix.chunbo.com/zabbix/api_jsonrpc.php', 'admin', 'Chunb0@2o14', '10.254.8.121', "system.cpu.util[,interrupt]")
    print c.getItemid() 
