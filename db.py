import json


class DB(object):
    """Used for working with json files"""
    def __init__(self, filename):
        self.json_file = filename

    def read_db(self):
        with open(self.json_file, 'r') as db_recs:
            recs = json.load(db_recs)
        return recs

    def write_db(self, data):
        with open(self.json_file, 'w') as db:
            db.seek(0)
            json.dump(data, db)

