import json


class LocCache:
    def __init__(self, commit_hash, commit_date, loc):
        self.commit_hash = commit_hash
        self.commit_date = commit_date
        self.loc = loc

    def toJSON(self):
        return json.dumps({
            'commit_hash': self.commit_hash,
            'commit_date': self.commit_date,
            'loc': self.loc
        })

    @classmethod
    def fromJSON(cls, string):
        json_data = json.loads(string)
        return cls(json_data['commit_hash'], json_data['commit_date'], json_data['loc'])