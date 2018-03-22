from jsonschema import validate
import json
class Validator:
    def validateRequest(self,req):
        try:
            validate(req, self.schema)
            return 0
        except Exception, e:
            return e.args[0]

    def readJson(self,jsonFile):
        self.schema=json.load(open(jsonFile))




class SchemaFiles:
    FILE1="a.json"
    FILE2="b.json"


