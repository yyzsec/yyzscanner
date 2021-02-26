import threading
from thirdparty import requests


# 定义多线程装饰器
def Threads(func):
    def decorator(*args, **kwargs):
        threads = []
        # 如果直接传一个int，那么直接开启多线程
        if isinstance(args[0], int):
            threadNum = args[0]
            for _ in range(threadNum):
                threads.append(threading.Thread(target=func))
        # 这是在Scanner模块里面给request留的多线程通道，方便传参
        else:
            threadNum = args[0].options.thread.threadNum
            for _ in range(threadNum):
                threads.append(threading.Thread(target=func, args=(args[0],)))
        for thread in threads:
            thread.daemon = True
            thread.start()
        threads[0].join()

    return decorator


# 定义C-c异常处理装饰器
def CatchKeyboardInterrupt(func):
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print("Canceled by user!!")

    return decorator


# 定义用于捕获请求异常的装饰器
def CatchRequestsExceptions(func):
    def decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print("Canceled by user!!")
            exit(1)

        except TimeoutError:
            print("Cross a TimeoutError")

        except ConnectionError:
            print("Cross a ConnectionError")

        except UnicodeDecodeError:
            print("Cross an UnicodeDecodeError")

        except StopIteration:
            print(''.ljust(110) + "\r", end='')

        except SystemExit:
            print("Exit signal has been called!")

        except requests.exceptions.ConnectionError:
            print("Cross a ConnectionError")

    return decorator


# 定义用于捕获请求异常的装饰器Async版
def CatchRequestsExceptionsAsync(func):
    async def decorator(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except KeyboardInterrupt:
            print("Canceled by user!!")
            exit(1)

        except TimeoutError:
            print("Cross a TimeoutError")

        except ConnectionError:
            print("Cross a ConnectionError")

        except UnicodeDecodeError:
            print("Cross an UnicodeDecodeError")

        except StopIteration:
            print(''.ljust(110) + "\r", end='')

        except SystemExit:
            print("Exit signal has been called!")
        # 由于aiohttp.client_exception.ServerDisconnectedError不能被捕获到，所以这里直接捕获所有异常
        except:
            print("Maybe crossed a ServerDisconnectedError")

    return decorator
