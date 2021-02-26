## 2月17日

上午考虑准备开始开发一个扫描器，大体要实现**dirsearch**的基本功能。

中午新建了文件夹，下载了**dirsearch**源码，准备开始开发。

下午看了一下源码，发现很多地方不懂，还是不习惯把类用到真实的环境中。

蒙了，补了一些类的开发知识，尝试用自己的想法加上在java中对类的认知去理解类在开发中的作用，写了和**dirsearch**差不多的入口，学习了优秀的框架代码的简洁明了（可能不是）。

## 2月18日

上午看了**optparse**的用法，发现在类Unix系统中参数的规范可以用到python里面来。

构建了如下模块

* --core

* ​    |--Controller.py

* ​    |--UrlHandler.py

* ​    |--ArgvParser.py

* ​    |--ThreadHandler.py

* ​    |--ExtensionHandler.py

* ​    |--UAHandler.py

* ​    |--DictHandler.py

除了Controller之外，其他的模块内容大体都差不多:

```python
class XXXHandler:
    def __init__(self, XXX):
        pass

    def getXXX(self):
        return self.XXX
```

后面觉得get方法有点没必要，但是又不想改了

大致逻辑是，程序运行的时候，启动**control**方法，依次处理传进来的参数：

```
ArgvParser --> 用optparse处理命令行传递的参数
UrlHandler --> url必须以http开头，并且默认在url后面加上斜杠/
ThreadHandler -->处理设置线程数量
ExtensionHandler --> 类似于dirsearch，也在字典后面加上%EXT%，让用户能够用上自定的拓展名
UAHandler --> 用户可以自己设置UA，不设置的话加上一个随机UA
DictHandler --> 处理自定义字典位置，以及初始化字典
```

学到的知识：

```python
1. Pycharm用的是PEP8代码风格规范，里面变量名必须小写，单词之间用下划线连接。（但是整个项目我还是打算用驼峰命名变量，因为自我感觉比较整洁规范好看）
2. 继续努力看源码
```

## 2月19日

打算把字典的读取处理了

```
1. 检测文件是否存在：
	os.access(filename, os.F_OK)
		第二个参数还有W_OK X_OK R_OK
2. with open() as fd:
	fd.read().splitlines()
	直接返回一个包括所有行的列表
	read是一次性读取完，所以，想到如果用户整个超大的字典，内存会不会爆掉呢？
	但是应该没有这么调皮的用户吧
3. open(filename, "r", errors="replace")里面的errors是遇到编码问题做处理的方式
	还可以errors=""
4. 初始化字典的时候考虑到要不要用正则表达式替换%EXT%呢
	直接replace要考虑到大小写，如果都转换成小写的话，对路径有没有影响呢
	测试了一下，在windows上不区分大小写，但是在linux下是要区分大小写的，所以，还是上正则吧Orz
	其实这里的正则没有那么难：
	        replaceEXT = re.compile(r"%ext%", re.IGNORECASE).sub
            self.wordList.append(replaceEXT(extension, each).strip())
	.sub是返回的一个函数，这个函数的作用是替换正则匹配的内容
	没想到不加括号的函数还能这样用
```

下午

```
1. 把打印banner和基本信息做好了
2. 把sb getXXX方法去掉了，直接获取属性即可
3. 新建了Scanner模块用于扫描器的请求
4. 属实没看懂dirsearch里面设置Header的方法：
    def setHeaders(self, key, value):
        self.headers[key.strip()] = value.strip() if value else value
	感觉后面的 if value else value多此一举
	可能是他开始调试用的，后面忘记删除了
5. 简单写了一下requests，单线程跑几分钟能把1w多的字典跑完，只处理了200和30x重定向
6. Pycharm里面的python console还挺好用的，可以看变量的各种属性
7. 着手开始搞定多线程，似乎遇到了问题，明天再来把。
```



## 2月22

```
1. 很久之前就突发奇想用装饰器来实现多线程，昨天晚上试了一下，居然成功了，今天早上来把代码实现了，其实麻烦的是参数传递，类里面的方法第一个参数必定是self，所以加了一个判断
# 定义多线程装饰器, 注意普通函数传递线程数量是放在参数第二个位置
def Threads(func):
    def decorator(*args, **kwargs):
        if isinstance(args[0], int):
            threadNum = args[0]
        else:
            threadNum = args[1]
        threads = []
        for _ in range(threadNum):
            threads.append(threading.Thread(target=func(args[0]))) //注意，这里的代码是错误的，当时没有注意到，后面才注意到的
        for thread in threads:
            thread.daemon = True
            thread.start()

    return decorator
    
2. 多线程出现了一点问题，字典迭代完了后程序直接退出了，但是请求还没请求完，这样一个结果都打印不出来，加一个while True即可！
3. 多线程没跑起来，debug了一下发现是装饰器的问题，装饰器里面的target传不了self参数，傻逼了
4. 改代码改了好久好久，改到最后发现tmd，target是可以传参的，在后面加个args=() 就解决了，傻了，改回原来简洁的代码
5. 处理了一下线程，加了join这样代码运行着优雅一点
6. 百度了一下如何实现单行覆盖打印，大概是这样的：
	sys.stdout.write(extension + " \r")
    sys.stdout.flush()
   但是出现了一点问题，大概就是，重新flush过后，前面点的会刷新，但是会在后面留下之前字符
   使用print("\r" + ''.ljust(110) + "\r", end='')
   ljust解决了
7. 打印彩色文字出问题了，一直不能成功
8. 放到linux里面跑出问题了，很卡，比单线程还卡
```

## 2月23

```
1. debug出结果了，结果join用错了，导致一直就只有一个线程在运行，傻了
2. 改了join，能够正常执行多线程了
3. 出大问题，python线程没用，dirsearch里面2个线程居然还比100个线程扫描完1w左右的字典来得快，之前就了解了python有GIL锁机制，还不信邪，结果多线程真的没用
	作者在https://github.com/maurosoria/dirsearch/issues/643里面也公开说到要把线程换成协程
   看来并不是我多线程写的有问题
4. 转战协程了，又从基础看了看，协程，生成器，迭代器
	1. 在python3.8后面不再用@asyncio.coroutine装饰器而改用async def（是不是3.8记不得了）
	2. async def里面不能用yeild from 语句
	3. 真牛逼啊真牛逼，看了点大佬写的文章还有《流畅的python》一书，真牛逼
5. 研究了一天协程，感觉是有点难的
```

## 2月24

```
1. 打算用2种方式，一是协程，二是线程
2. 增加了智能扫描，避免遇到访问某些网站不存在的url返回的都是200状态码
	智能扫描最开始会请求一个任意url，如果遇到200或者跳转，然后后续的会根据每次请求返回的Content-length与第一次请求的对比，如果差不多(±3)，则忽略这个请求
3. 协程里面用aiohttp.get()有很多是跟之前requests不一样的，遇到了一些问题，但是都马马虎虎的解决了
4. 很多aiohttp里面的Exception都不能被捕获到：
	aiohttp.client_exceptions.ServerDisconnectedError
	捕获不到，自己抛不出来，只有except Exception处理了。。
5. 知道了很重要的一件事，就是捕获异常的时候，一定不要忽略
	except KeyboardInterrupt
	而且要注意exit(code) sys.exit(code) 是raise SystemExit异常，不能给捕获了
	不然很多时候不能正常退出程序
6. “不需要在每个可能出错的地方去捕获错误，只要在合适的层次去捕获错误就可以了。这样一来，就大大减少了写try...except...finally的麻烦。”明天改一改那些异常捕获语句，感觉是有点多了。
```

## 2月25

```
1. 知道了在线程里面捕获KeyboardInterrupt是杀不死Thread里面的线程的，因为KeyboardInterrupt只能在main线程里面被捕获到
2. 我的程序不能捕获到KeyboardInterrupt的主要原因是因为线程用了.join()，所以其实已经捕获到了，但是被join方法block了，所以只有等待join结束后才能抛出异常
3. 为了方便捕获并处理异常，写了几个装饰器：
	@CatchKeyboardInterrupt
	@CatchRequestsExceptions
	@CatchRequestsExceptionsAsync
4. 在给多线程requests加上装饰器的时候遇到了2个装饰器碰在一起的情况了，这里顺序是有规定的，顺序不同，执行的结果就不一样
	@Threads
    @CatchRequestsExceptions
    def requester(self):
    debug了一下，只有这种顺序是能同时开启多线程并且正确处理异常的
```

