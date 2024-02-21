import requests


class fileClient():
    def __init__(self, serverIp='0.0.0.0', port=8080, command=None):
        self.ip = serverIp
        self.port = port
        self.cmd = command
        self.time = None

    def requestServer(self):
        url = 'https://{}:{}?cmd={}&time={}'
        result = requests.get(url=url)
