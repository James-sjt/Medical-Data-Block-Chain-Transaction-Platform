import json


class transaction:
    def __init__(self, filename, uploader, hash, timestamp, pre_owner, current_owner, trans_type):
        self.filename = filename
        self.uploader = uploader
        self.hash = hash
        self.timestamp = timestamp
        self.pre_owner = pre_owner
        self.current_owner = current_owner
        self.trans_type = trans_type


class TransactionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, transaction):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

