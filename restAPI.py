from flask import Flask, request
from handler import Handler
app = Flask(__name__)

@app.route("/", methods=['post'])
def getInfo():
    x=Handler()
    response =x.handleRequest(request.data)


    # return "hello", 200
    if not response['rc']:
        return str(response["output"]), 200
    else :
        return str(response["errorMsg"]), 400
if __name__ == '__main__':
    app.run(debug=True)