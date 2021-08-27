import socket



host_name = 'www.baidu.com'
addr = socket.gethostbyname(host_name)
print(host_name+' \'s name is '+addr)
