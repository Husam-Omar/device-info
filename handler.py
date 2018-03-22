from infrastructure import *
import json
import gc
from validator import *

class ReturnKeys:
    RETURN_CODE="rc"
    ERROR_MESSAGE="errorMsg"
    OUTPUT="output"

class Handler:
    def __init__(self):
        self.driver=LinuxServerDriver()
        self.method = {
            Methods.GET_CPU: self.driver.getCpu,
            Methods.GET_CPU_DETAILS: self.driver.getCpuDetails,
            Methods.GET_MEMORY: self.driver.getMemory,
            Methods.GET_DISK_SPACE: self.driver.getDiskSpace,
            Methods.GET_HOSTNAME: self.driver.getHostname
        }



    def handleRequest(self, req):
        validate = Validator()
        d= json.loads(req)
        if d["method"] == Methods.GET_CPU_DETAILS:
            validate.readJson(SchemaFiles.FILE2)
        else:
            validate.readJson(SchemaFiles.FILE1)
        ret=validate.validateRequest(d)
        if not ret:
            result = self.method[d["method"]](**d)
            return self.handleResponse(result)
        else:
            res=[]
            res.append(500)
            res.append(ret)
            return self.handleResponse(res)

    def handleResponse(self,result):
        if result[0]:
            #rc>0  error
            jsn={}
            jsn[ReturnKeys.RETURN_CODE]=result[0]
            jsn[ReturnKeys.ERROR_MESSAGE]=result[1]
            # return json.dumps(jsn)
            return jsn
        else:
            #rc=0 success
            jsn={}
            jsn[ReturnKeys.RETURN_CODE]=result[0]
            jsn[ReturnKeys.OUTPUT]=result[1]
            # return json.dumps(jsn)
            return jsn

    def __del__(self):
        self.driver=None
        self.method=None
        del self.driver
        del self.method
        gc.collect()
