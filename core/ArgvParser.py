from optparse import OptionParser


# 处理命令行参数
class ArgvParser:
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-u", "--url", dest="url",
                          help="Target url you want to scan.", type="string")
        parser.add_option("-t", "--thread", dest="threadNum",
                          help="Thread number you want to use.", type="int")
        parser.add_option("-e", "--extension", dest="extensions",
                          help="Extension list separated by commas (Example: -e php,asp)")
        parser.add_option("-U", "--user-agent", type="string", dest="useragent",
                          help="Use your own User-Agent. if not provided, we will use a random UA.")
        parser.add_option("-c", "--cookies", type="string", dest="cookies",
                          help="Set your cookies.(Example: -c 'user=admin; password=123456') ")
        parser.add_option("-d", "--dictionary", type="string", dest="dictionary",
                          help="Set your dictionary.")
        parser.add_option("--async", type="int", dest="asyncTag",
                          help="if --async=1, we will use async instead of Threads. (Very fast, use carefully!).")
        (self.options, self.args) = parser.parse_args()
        if not self.options.url:
            OptionParser().print_help()
            exit(1)
