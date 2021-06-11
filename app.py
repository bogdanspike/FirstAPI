from flask import Flask,request
from reader import Reader

app=Flask(__name__)

@app.route("/home")
def hello():
    return "Salutari,astronautule!", 200

@app.route("/first", methods=['GET','POST','DELETE'])
def first():
    if request.method == 'GET':
        return "a"

    elif request.method == 'POST':
        return "b"

    elif request.method == 'DELETE':
        return "c"

if __name__ == '__main__':
    app.run()