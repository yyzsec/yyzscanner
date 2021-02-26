from thirdparty import requests
from core.UAHandler import UAHandler
from core.ThreadHandler import runner
from core.Decorators import Threads, CatchRequestsExceptions


class Scanner:
    def __init__(self, options):
        self.options = options
        self.randomUrlLength = 0
        self.progress = 0
        self.asyncTag = options.asyncTag
        self.headers = {
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }

        if self.options.cookies:
            self.setHeaders("Cookie", self.options.cookies)

        self.Lists = iter(self.options.wordlist)
        if self.fuzzer():
            if self.asyncTag == 1:
                runner(self)
            else:
                self.requester()

    @Threads
    @CatchRequestsExceptions
    def requester(self):
        while True:
            if self.options.ua.randomTag:
                self.setHeaders("User-Agent", UAHandler.getRandomUA())
            extension = next(self.Lists)
            response = requests.get(self.options.url + extension, headers=self.headers, allow_redirects=False)
            percent = str(int(round(self.progress) / round(len(self.options.wordlist)) * 100))
            print(percent + "%   " + extension.ljust(110) + "\r", end='')
            self.progress += 1
            if self.randomUrlLength:
                if not ((self.randomUrlLength - 3) <= len(response.content) <= (self.randomUrlLength + 3)):
                    self.options.printer.printLine(response)
            else:
                self.options.printer.printLine(response)

    def setHeaders(self, key, value):
        self.headers[key.strip()] = value.strip()

    def fuzzer(self):
        try:
            if self.options.ua.randomTag:
                self.setHeaders("User-Agent", UAHandler.getRandomUA())
            res = requests.get(self.options.url + "Ws000s2ds3pa3oskS1.php", headers=self.headers, allow_redirects=False)
            if res.status_code != 404:
                print("该目标启用了任意URL返回200， 或者进行跳转")
                if input("宁是否需要启用智能扫描：(y/n)") in ["y", "Y", "Yes", "YES", "yes"]:
                    self.randomUrlLength = len(res.content) + 1
                else:
                    print("Canceled by user!")
                    exit(1)

        except requests.exceptions.SSLError:
            print("SSL连接失败，请检查！")
            exit(1)
        except requests.exceptions.ConnectionError:
            print("连接失败，请检查与目标的连通性！")
            exit(1)
        except KeyboardInterrupt:
            print("Canceled by user!")
            exit(1)
        return 1
