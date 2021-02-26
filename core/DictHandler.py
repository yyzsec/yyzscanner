import os
import re
import urllib.parse


class DictHandler:
    def __init__(self, dictionaryPath, extensions):
        # 设置默认字典为db/dicc.txt
        if dictionaryPath is None:
            self.dictionaryPath = "db/dicc.txt"
        else:
            # 检测用户给出的字典是否存在
            if self.exists(dictionaryPath):
                self.dictionaryPath = dictionaryPath
            else:
                print("Dictionary file do not exists.")
        self.extensions = extensions
        self.wordList = []
        self.initDict()

    # 初始化字典
    def initDict(self):
        # 先读取所有行放进一个列表
        lines = self.getLines(self.dictionaryPath)
        # 初始化正则替换函数
        replaceEXT = re.compile(r"%ext%", re.IGNORECASE).sub
        for each in lines:
            # urlencode
            quoted = self.quote(each)
            # 判断后缀名是否需要用户自定，如果是，则替换后缀名后加入字典列表，否则直接加入字典列表
            if "%ext%" in each.lower():
                for extension in self.extensions:
                    self.wordList.append(replaceEXT(extension, quoted).strip())
            else:
                self.wordList.append(quoted)

    # 检测文件是否存在
    @staticmethod
    def exists(fileName):
        return os.access(fileName, os.F_OK)

    # 获取字典返回一个列表
    @staticmethod
    def getLines(fileName):
        with open(fileName, "r", errors="replace") as fd:
            lines = fd.read().splitlines()
            return lines

    # urlencode
    @staticmethod
    def quote(string):
        return urllib.parse.quote(string, safe="!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
