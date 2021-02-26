YYZScanner- A Simple Web Path Scanner
=========

![Build](https://img.shields.io/badge/Built%20with-Python-Blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/release/xiaoyaovo/yyzscanner.svg)
![Stars](https://img.shields.io/github/stars/xiaoyaovo/yyzscanner.svg)

 **Current Release: v0.0.1 (2021.2.25)**


Overview
--------
- 这是一个由yyz开发的自用的目录扫描工具
- Based on Python3.x
- 于2021.2.25为期一周开发完成
- 学习中，代码或者措辞有任何问题请告知，感激不尽！！


Installation & Usage
------------

```python
git clone https://github.com/xiaoyaovo/yyzscanner.git
cd yyzscanner
python3 main.py -u <URL>
```


Features
--------
- 支持[协程与异步](#Async)处理快速扫描
- 支持[多线程](#Threads)处理快速扫描
- 支持自定义UA，不设置的话默认使用随机UA
- 支持自定义Cookie
- 支持类似于dirsearch一样的自定义后缀名并自动加入扫描[wordlists](#wordlists).
- 支持[智能扫描](#SmartScan)

Options
-------


```
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     Target url you want to scan.
  -t THREADNUM, --thread=THREADNUM
                        Thread number you want to use.
  -e EXTENSIONS, --extension=EXTENSIONS
                        Extension list separated by commas (Example: -e
                        php,asp)
  -U USERAGENT, --user-agent=USERAGENT
                        Use your own User-Agent. if not provided, we will use
                        a random UA.
  -c COOKIES, --cookies=COOKIES
                        Set your cookies.(Example: -c 'user=admin;
                        password=123456')
  -d DICTIONARY, --dictionary=DICTIONARY
                        Set your dictionary.
  --async=ASYNCTAG      if --async=1, we will use async instead of Threads.
                        (Very fast, use carefully!).
```

### wordlists

字典是使用的dirsearch内置的字典，类似dirsearch，在使用时可自定义后缀名扫描

例如，如果你的字典长这样

```
admin/
index.%EXT%
```

那么使用了`-e php,asp,txt`，则字典会自动扩充为

```
admin/
index.php
index.asp
index.txt
```

### Simple usage

```
python3 dirsearch.py -u https://target
```

```
python3 dirsearch.py -u https://target -e * --async=1
```

```
python3 dirsearch.py -u https://target -e php,html,js -d /usr/lib/wordlist
```

### Threads
关于多线程，实际上在测试的时候多线程并不能提供我们速度上显著的帮助，默认20即可

> 如果自定义线程的话，建议不要设置得太大。

### Async

推荐大家使用异步处理请求，异步的速度会比多线程快很多，添加参数`--async=1`

但是注意异步请求的速度比多线程实在是快太多了，以至于请求速度很快，请大家小心使用并时刻注意与目标机器的连通性。

> 在异步里面我把控制并发数的变量值设置成了线程数量的值，也就是说，你可以在使用异步的时候同时设置 -t 50这样会比默认的20来得稍微快一点点，但是也不明显

### SmartScan

之前在看dirsearch的时候看到了有个启发式扫描

仔细看了一下，原来在访问某些网站不存在的url的时候，服务端返回的都是200状态码或者一个30x跳转

基于此，智能扫描最开始会请求一个任意url，如果遇到200或者跳转，然后后续的会根据每次请求返回的Content-length与第一次请求的对比，如果差不多(±3)，则忽略这个请求

## Some thoughts

### Threads

在开发多线程之前看了一下python里面实现多线程的概况

1. CPython解释器中存在的全局解释器锁定（Global Interpreter Lock，GIL）

   使得多线程在python3.x中感觉是个笑话，具体可以看[这个](https://www.zhihu.com/question/23474039)

2. 那为什么dirsearch中还是实现了多线程，我感觉可能有些机器是用的PyPy或者JPython解释器

   但是作者在[issue](https://github.com/maurosoria/dirsearch/issues/643)中也写到了未来要把多线程换成异步

3. 这个扫描器是IO密集型代码，所以在请求和处理请求的时间大大增加也会导致Python的多线程与单线程运行时间无异

4. 于是，我同时完成了多线程与异步版本

### Exception

异常处理有时候是比较麻烦的一件事

* **KeyboardInterrupt**

这个异常是用户在Ctrl-C后需要抛出来的，但是

1. 他在多线程中启用join后是抛不出来的
2. 如果想要在以上情况中抛出来，那么必须设置join的timeout参数，例如`thread.join(1)`，timeout就是指这个线程每次最多可以使用CPU的时间
3. 如果设置join参数，那么遇到网络不好的时候，扫描开始几秒钟后程序会退出
4. 在很多地方都需要抛出这个异常，为此，我设计了几个比较方便捕获异常的装饰器
5. 这个异常与**SystemExit**异常都是比较特殊的异常，不继承于Exception而是BaseException，在Exception不会被捕获到，所以，不能直接except Exception而是需要将每一个异常精确的捕获

以及在开发异步的时候遇到的异常：

* **aiohttp.client_exceptions.ServerDisconnectedError**

该异常是不能精确的捕获到的，因为是在异步函数里面抛出来的

> 异步函数感觉跟普通的函数有很大的区别，比如实现装饰器的时候不能直接挂一个装饰器在函数头上，而是需要自己写异步专属的装饰器

### Decorators

在开发过程中，自己写了几个装饰器是感觉到比较快乐的，其中也遇到了很多问题。

我定义了如下几个装饰器：

```python
# 定义多线程装饰器
def Threads(func):
    def decorator(*args, **kwargs):
        pass
    return decorator
# 定义C-c异常处理装饰器
def CatchKeyboardInterrupt(func):
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            pass
    return decorator
# 定义用于捕获请求异常的装饰器
def CatchRequestsExceptions(func):
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            pass
    return decorator
# 定义用于捕获请求异常的装饰器Async版
def CatchRequestsExceptionsAsync(func):
    async def decorator(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except:
            pass
    return decorator
# pass里面是具体的代码
```

1. 写异常处理的装饰器的初衷是能够方便抛出异常

2. 但是在处理异步请求的时候，普通的装饰器是不能用的，于是写了2个版本的处理requests异常的装饰器

3. 在多线程函数上方由于要使用多线程装饰器，还要使用异常捕获装饰器，所以遇到了2个装饰器共用的情况，这个时候其实是比较复杂的，因为装饰器放置的前后顺序会影响到代码运行的结果，网上也有很多生动的讲解，这里我偷个懒，把2个顺序都debug一下，能够正确处理异常并且开启多线程的那个就留下了：

   ```python
   @Threads
   @CatchRequestsExceptions
   def requester(self):
       pass
   ```

4. 最开始写多线程装饰器的时候，没有做好多线程函数传参的工作（后面发现只需要添加args=(self,)即可），然后需要装饰类里面的成员方法，但是也没写过类装饰器，实在是想偷懒，所以就一直在解决传参的问题，还好搜了一下，不然又会延长开发周期，希望以后能接触到类的装饰器。

## Known Bugs && Next Step

* 在经过很长时间的多线程扫描结束过后不能正常退出，请手动退出
* 多线程暂时不能Ctrl-C退出
* 在处理打印颜色上暂时遇到了问题，预计在V0.0.2里面完成
* 将使用更多http-method 比如 POST HEAD

## Reference & Appreciation

> [dirsearch](https://github.com/maurosoria/dirsearch) - Web path scanner

刚开始是没有写过Python的项目的，就直接看的dirsearch的源码，在这里谢谢大佬们贡献的优秀工具，能够学到很多，包括一些开发规范，框架总体结构，函数，类，第三方库的用法，还有一些代码里面的小trick等等，十分的感谢，自己也对dirsearch的用法有了更深入的了解，在未来的安全工作中一定能对自己有所启发，鞠躬！！
