import json
import time
import urllib.request, urllib.error, urllib.parse

class IFTTTOutput:
    url_template = 'https://maker.ifttt.com/trigger/{name}/with/key/{key}'

    def __init__(self, config):
        self.key = config['api_key']

    def trigger(self, cmd, custom = None):
        data = dict(zip(['value1','value2','value3'], custom))
        data_bytes = json.dumps(data).encode('ascii')
        url = self.url_template.format(name = cmd, key = self.key)
        print("Requesting {}".format(url))
        req = urllib.request.Request(url, data_bytes, {'Content-Type': 'application/json'})
        f = urllib.request.urlopen(req)
        response = f.read()
        f.close()
        return response


