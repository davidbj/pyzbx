介绍
=========

pyzbx 使用python开发获取zabbix 源数据的API Application.


###版本
0.0.1

###功能
  目前该APP提供一些获取zabbix 数据的interface,具体功能如下:
  
* [getAuthCode()] - 用户获取登入用户的Auth摘要.
* [getHostid()] - 通过参数hostname,获取该hostname的hostid.
* [getItemid()] - 获取item 的itemid.
* [getHistoryData()] - 获取历史数据.具体的参数可以参考:<a>https://www.zabbix.com/documentation/2.0/manual/appendix/api/history/get</a>


###安装
```sh
$ pip install pyzbx
```

###实例

```sh
$ response = pyzbx.ZbxAPI(zabbix_url="http://zabbix_server[:port]/zabbix/api_jsonrpc.php", user='user', password='password')
$ auth = response.getAuthCode()                              #获取登入用户的Auth摘要
$ hostid = response.getHostid(monitor_hostname='x.x.x.x')    #获取item 监控主机的hostid
$ itemid = response.getItemid(monitor_item_key='system.cpu.util[,steal]',https://www.zabbix.com/documentation/2.0/manual/appendix/api/history/get)                            #获取item 监控项的itemid
$ historyData = response.getHistoryData()                    #获取zabbix Server的历史记录
```

###关于作者@<b>shaozhi.zhang</b>

<b>Email: </b> davidbjhd@gmail.com
-----
<b>Blog: </b>  http://www.devops.com
-----
