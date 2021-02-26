class ExtensionHandler:
    def __init__(self, extensions):
        self.extensions = extensions
        if self.extensions == "*":
            self.extensions = [
                "php", "inc.php", "jsp", "jsf", "asp", "aspx", "do", "action", "cgi",
                "pl", "html", "htm", "js", "css", "json", "txt", "tar.gz", "tgz"
            ]
        elif self.extensions is not None:
            self.extensions = extensions.split(",")
        else:
            self.extensions = [
                "php",  "jsp", "asp", "html", "js", "css", "txt"
            ]
