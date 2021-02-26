import asyncio
import aiohttp
from core.UAHandler import UAHandler
from core.Decorators import CatchKeyboardInterrupt, CatchRequestsExceptions, CatchRequestsExceptionsAsync


class ThreadHandler:
    def __init__(self, threadNum):
        # 简单判断线程大小的正负，设置默认值
        if threadNum is not None:
            if threadNum <= 0:
                print("Threads should greater than ZERO")
                exit(1)
            else:
                self.threadNum = threadNum
        else:
            self.threadNum = 20


# 下面三个协程的方法是连起来用的，都是协程扫描的主逻辑
@CatchRequestsExceptionsAsync
async def requester(session, extension, Scanner):
    if Scanner.options.ua.randomTag:
        Scanner.setHeaders("User-Agent", UAHandler.getRandomUA())

    async with session.get(Scanner.options.url + extension, headers=Scanner.headers,
                           allow_redirects=False) as response:
        percent = str(int(round(Scanner.progress) / round(len(Scanner.options.wordlist)) * 100))
        print(percent + "%   " + extension.ljust(110) + "\r", end='')
        Scanner.progress += 1
        if Scanner.randomUrlLength:
            if not ((Scanner.randomUrlLength - 5) <= len(await response.text()) <= (Scanner.randomUrlLength + 5)):
                Scanner.options.printer.asyncPrintLine(response)
        else:
            Scanner.options.printer.asyncPrintLine(response)


async def main(Scanner):
    extensions = Scanner.options.wordlist
    conn = aiohttp.TCPConnector(limit=Scanner.options.thread.threadNum)
    async with aiohttp.ClientSession(connector=conn) as session:
        await fetch_multi(session, extensions, Scanner)


async def fetch_multi(session, extensions, Scanner):
    tasks = []
    for extension in extensions:
        task = asyncio.create_task(requester(session, extension, Scanner))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


@CatchKeyboardInterrupt
def runner(Scanner):
    eventLoop = asyncio.get_event_loop()
    eventLoop.run_until_complete(main(Scanner))
    print(''.ljust(110), end='')
