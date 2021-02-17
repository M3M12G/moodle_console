import json


class DB(object):
    """
    Used for working with json files
    The class that works as a DB connection
    """

    def __init__(self, filename):
        self.json_file = filename

    def read_db(self):
        with open(self.json_file, 'r') as db_recs:
            recs = json.load(db_recs)
        return recs

    def write_db(self, data):
        with open(self.json_file, 'w') as db:
            db.seek(0)
            json.dump(data, db, indent=2)

'''
test = DB("test.json")
test_dict = {}
test_dict["courses"] = []
test_dict["courses"].append({
    "name": "python",
    "teacher": "sh_a",
    "total": 20
})
test_dict["courses"].append({
    "name": "c#",
    "teacher": "a_kh",
    "total": 20
})
test_dict["courses"].append({
    "name": "OS",
    "teacher": "z_b",
    "total": 20
})

data = test.read_db()
data["student"].append({
      "id": "login+role2",
      "name": "name2",
      "surname": "surname2",
      "login": "login2",
      "role": "student"
})
test.write_db(data)
'''
#print(test.read_db()["student"])