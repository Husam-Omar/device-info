from handler import Handler
import gc


# gc.set_threshold(1)
# gc.enable()
while 1:
    request= raw_input("enter json request: ")
    if not request:
        break
    x=Handler()
    response=x.handleRequest(request)
    del x
    print str(response)
