from core.UrlHandler import UrlHandler
from core.ExtensionHandler import ExtensionHandler
from core.UAHandler import UAHandler
from core.ThreadHandler import ThreadHandler
from core.DictHandler import DictHandler
from core.Printer import Printer
from core.Scanner import Scanner
import time


class Controller:
    def __init__(self, options):
        # 实例化打印类
        self.printer = Printer()
        # 处理url
        self.url = UrlHandler(options.url).url
        # 实例化线程类
        self.thread = ThreadHandler(options.threadNum)
        # 处理后缀名
        self.extensions = ExtensionHandler(options.extensions).extensions
        # 实例化User-Agent类
        self.ua = UAHandler(options.useragent)
        # 处理cookies
        self.cookies = options.cookies
        # 处理后缀名并且生成字典
        self.wordlist = DictHandler(options.dictionary, self.extensions).wordList
        # 是否开启协程扫描
        self.asyncTag = options.asyncTag
        # 开始扫描
        self.start()

    def start(self):
        # 开始打印banner以及基本信息
        self.printer.begin(self)
        # 扫描开始
        Scanner(self)
        # 打印扫描结束
        self.printer.end(self)
