import sys
import time


class Printer:
    def __init__(self):
        self.BANNER = """ __   __ __   __   ____    ___     ___     ___    _  _    _  _     ___     ___   
 \ \ / / \ \ / /  |_  /   / __|   / __|   /   \  | \| |  | \| |   | __|   | _ \  
  \ V /   \ V /    / /    \__ \  | (__    | - |  | .` |  | .` |   | _|    |   /  
  _|_|_   _|_|_   /___|   |___/   \___|   |_|_|  |_|\_|  |_|\_|   |___|   |_|_\  
_| ''' |_| ''' |_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'  @yyz"""

        self.MWZZ = """                               ,''`.,./.                            
                             ,'        Y','..                       
                           ,'           \  | \                      
                          /              . |  `                     
                         /               | |   \                    
            __          .                | |    .                   
       _   \  `. ---.   |                | j    |                   
      / `-._\   `Y   \  |                |.     |                   
     _`.    ``    \   \ |..              '      |,-'''7,....        
     l     '-.     . , `|  | , |`. , ,  /,     ,'    '/   ,'_,.-.   
     `-..     `-.  : :     |/ `   ' '\,' | _  /          '-'    /___
      \\''' __.,.-`.: :        /   /._    l'.,'                      
       `--,   _.-' `'.           /__ `'-.' '         .              
       ,---..._,.--'''''''--.__..----,-.'   .  /    .'   ,.--       
       |                          ,':| /    | /     ;.,-'--      ,.-
       |     .---.              .'  :|'     |/ ,.-=''-.`'`' _   -.' 
       /    \    /               `. :|--.  _L,'---.._        '----' 
     ,' `.   \ ,'           _,     `''   ``.-'       `-  -..___,'   
    . ,.  .   `   __     .-'  _.-           `.     .__    \         
    |. |`        '  ;   !   ,.  |             `.    `.`'---'        
    ,| |C\       ` /    | ,' |(]|            -. |-..--`             
   /  ''--'       '      /___|__]        `.  `- |`.                 
  .       ,'                   ,   /       .    `. \                
    \                      .,-'  ,'         .     `-.               
     x---..`.  -'  __..--''/'''''  ,-.      |   |   |               
    / \--._'-.,.--'     _`-    _. ' /       |     -.|               
   ,   .   `-..__ ...--'  _,.-' | `   ,.-.  ;   /  '|               
  .  _,'         ''-----''      |    `   | /  ,'    ;               
  |-'  .-.    `._               |     `._// ,'     /                
 _|    `-'   _,' '`--.._________|        `,'    _ /.                
//\   ,-._.''/\__,.   _,'     /_\__/`. /'.-.'.-/_,`-' yyz            
`-'`'' v'    `'  `-`-'              `-'`-`                          """

    def banner(self):
        print(self.MWZZ)
        print("YYZ_scanner启动！\n")
        # print(self.BANNER)

    @staticmethod
    def begin(options):
        options.printer.banner()
        print("Target URL: " + options.url)
        print()
        print("Extensions: " + str(options.extensions), end=" | ")
        print("Wordlist Size: " + str(len(options.wordlist)), end=" | ")
        print("Threads: " + str(options.thread.threadNum), end=" | ")
        print("Use cookies: True", end=" | ") if options.cookies \
            else print("Use cookies: False", end=" | ")
        print("User-Agent: " + "Random", end='') if options.ua.randomTag \
            else print("User-Agent: " + options.ua.ua, end='')
        print(" | async\n") if options.asyncTag else print("\n")
        print("Task begin!")
        options.startTime = time.time()

    @staticmethod
    def end(options):
        sys.stdout.write("\r")
        sys.stdout.flush()
        print()
        print("Task completed!")
        # 结束计时
        print("用时(s): " + str(time.time() - options.startTime))

    @staticmethod
    def printLine(res):
        if res.status_code == 200:
            print(f"[*]   {res.request.path_url} 200")
        elif 300 < res.status_code < 310:
            print(f"[*]   {res.request.path_url} --> {res.headers['Location']} {str(res.status_code)}")

    @staticmethod
    def asyncPrintLine(res):
        if res.status == 200:
            print(f"[*]   {res.url} 200")
        elif 300 < res.status < 310:
            print(f"[*]   {res.url} --> {res.headers['Location']} {str(res.status)}")
