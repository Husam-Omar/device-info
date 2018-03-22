import paramiko
import re
import gc

class LinuxCommands:
    CPU_INFO='cat /proc/cpuinfo'
    MEMORY_INFO='free'
    HARDDISK_INFO='df'
    HOSTNAME='hostname'

class RequestAttributes:
    SERVER="server"
    USER="user"
    PASSWORD="password"
    CPU_NAME="cpuName"

class Methods:
    GET_CPU="getCpu"
    GET_CPU_DETAILS="getCpuDetails"
    GET_MEMORY="getMemory"
    GET_DISK_SPACE="getDiskSpace"
    GET_HOSTNAME="getHostname"




class LinuxServerDriver:
    def connect(self, server, user, password):
        self.server =server
        self.user=user
        self.password=password
        self.client =paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.server, username=self.user, password=self.password)
        except Exception :
            rc=1
            errorMsg="cannot connect to server"
            return (rc,errorMsg)
        return 0
    def getCpu(self, **data):
        server=data[RequestAttributes.SERVER]
        user=data[RequestAttributes.USER]
        password=data[RequestAttributes.PASSWORD]
        dictionary={}
        rc=1
        errorMsg = ""
        connectoinResult=self.connect(server, user, password)
        if not connectoinResult:
            stdin, stdout, stderr = self.client.exec_command(LinuxCommands.CPU_INFO)
            output = stdout.readlines()
            i=0
            for x in output:
                st=x.encode('utf-8')
                if st.find("model name") > -1:
                    dictionary[i]=str(st[13:]).strip()
                    i+=1
                    rc=0
            if rc :
                error = stderr.readlines()
                # i=0
                errorMsg=str(error)
                self.client.close()
                return (rc, errorMsg)
            self.client.close()
            return (rc,dictionary)
        else:
            return connectoinResult
    def getCpuDetails(self, **data):
        server=data[RequestAttributes.SERVER]
        user=data[RequestAttributes.USER]
        password=data[RequestAttributes.PASSWORD]
        cpuName=data[RequestAttributes.CPU_NAME]
        dictionary={}
        rc=1
        errorMsg = ""
        connectoinResult = self.connect(server, user, password)
        if not connectoinResult:
            stdin, stdout, stderr = self.client.exec_command(LinuxCommands.CPU_INFO)
            output = stdout.readlines()
            self.flag=0
            for x in output:
                st= x.encode('utf-8')
                if st.find("processor	: "+str(cpuName)) > -1:
                    self.flag=1

                if st.find("processor	: "+str(cpuName+1)) > -1:
                    self.flag=0
                if self.flag ==1 :
                    objj=re.match(r'(.+):(.+)',st)
                    if objj and objj.group(1).find("power")<0 :
                        dictionary[objj.group(1)]=objj.group(2)
                    rc=0
            if rc :
                error = stderr.readlines()
                errorMsg=str(error)
                self.client.close()
                return (rc, errorMsg)
            self.client.close()
            return (rc, dictionary)
        else:
            return connectoinResult
    def getMemory(self, **data):
        server=data[RequestAttributes.SERVER]
        user=data[RequestAttributes.USER]
        password=data[RequestAttributes.PASSWORD]
        dictionary={}
        rc=1
        errorMsg = ""
        connectoinResult = self.connect(server, user, password)
        if not connectoinResult:
            stdin, stdout, stderr = self.client.exec_command(LinuxCommands.MEMORY_INFO)
            output = stdout.readlines()
            for x in output:
                st= x.encode('utf-8')
                objj= re.match(r'Mem:\s+(\w+)\s+(\w+)\s+(\w+)', st)
                if objj:
                    dictionary["total"]=objj.group(1)
                    dictionary["free"]=objj.group(2)
                    dictionary["used"]=objj.group(3)
                    rc=0
            if rc :
                error = stderr.readlines()
                # i=0
                errorMsg=str(error)
                self.client.close()
                return (rc, errorMsg)
            self.client.close()
            return (rc,dictionary)
        else:
            return connectoinResult
    def getDiskSpace(self, **data):
        server=data[RequestAttributes.SERVER]
        user=data[RequestAttributes.USER]
        password=data[RequestAttributes.PASSWORD]
        dictionary={}
        rc=1
        errorMsg = ""
        connectoinResult = self.connect(server, user, password)
        if not connectoinResult:
            stdin, stdout, stderr = self.client.exec_command(LinuxCommands.HARDDISK_INFO)
            output = stdout.readlines()
            for x in output:
                st= x.encode('utf-8')
                objj= re.match(r'/dev/sda1 \s+\w+\s+(\w+)\s+(\w+)\s+(\w+)%', st)
                if objj:
                    dictionary["used"]=objj.group(1)
                    dictionary["available"]=objj.group(2)
                    dictionary["use"]=objj.group(3)+"%"
                    rc=0
            if rc :
                error = stderr.readlines()
                # i=0
                errorMsg=str(error)
                self.client.close()
                return (rc, errorMsg)
            self.client.close()
            return (rc,dictionary)
        else:
            return connectoinResult
    def getHostname(self, **data):
        server=data[RequestAttributes.SERVER]
        user=data[RequestAttributes.USER]
        password=data[RequestAttributes.PASSWORD]
        dictionary={}
        rc=1
        errorMsg=""
        connectoinResult = self.connect(server, user, password)
        if not connectoinResult:
            stdin, stdout, stderr = self.client.exec_command(LinuxCommands.HOSTNAME)
            output = stdout.readlines()
            i = 0
            for x in output:
                st = x.encode('utf-8')
                dictionary[i] = str(st).strip()
                i += 1
                rc = 0
            if rc:
                error = stderr.readlines()
                # i=0
                errorMsg=str(error)
                self.client.close()
                return (rc, errorMsg)
            self.client.close()
            return (rc, dictionary)
        else :
            return connectoinResult

