class UrlHandler:
    def __init__(self, url):
        self.url = url
        if not self.url.endswith("/"):
            self.url += "/"
        self.handleProtocol()

    def handleProtocol(self):
        if not self.url.startswith("http"):
            print("Url should start with http or https!")
            exit(1)
