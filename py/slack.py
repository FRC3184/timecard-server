import urllib.request
import json
import config


def send_message(message, url=None):
    if config.slack_webhook_incoming is None:
        return None
    req = urllib.request.Request(config.slack_webhook_incoming)
    data = {"text": message}

    return urllib.request.urlopen(req, json.dumps(data).encode("utf-8"))
