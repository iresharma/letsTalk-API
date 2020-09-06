from flask import Flask
from flask_cors import CORS
from flask import request
from flask import json

from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import send

from db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mahesh-01022001'
CORS(app = app)

socket = SocketIO(app)

socket.init_app(app = app, cors_allowed_origins="*", debug= True)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    args = request.args
    if request.method == 'GET':
        print(args['token'])
        uid = checkToken(args['token'])
        if(uid):
            user = getUser(uid)
            if(user):
                return json.jsonify(user), 200
            else:
                return json.jsonify(
                    {
                        'error': 'User Not Found error'
                    }
                ), 401
        else:
            return json.jsonify(
                {
                    'error': 'Invalid token login again'
                }
            ), 401
    elif request.method == 'POST':
        data = request.form
        print(data)
        if( '@' in data['id']):
            user = emailLogin(data['id'], data['password'])
        else:
            user = usernamelogin(data['id'], data['password'])
        if(user == 'Not found'):
            return json.jsonify(
                {
                    'error': 'User Not Found error'
                }
            ), 401
        elif(user):
            user['_id'] = str(user['_id'])
            token = reassignToken(user['_id'])
            return json.jsonify(
                {
                    'data': user,
                    'token': token
                }
            ), 200
        else:
            return json.jsonify(
                {
                    'error': 'User authentication error'
                }
            ), 401

            
@app.route('/register', methods = ['POST'])
def register():
    data = request.form
    user, token = createUser(data)
    print(user)
    if user: 
        return json.jsonify(
            {
                'uid': user,
                'token': token
            }
        ), 200
    else:
        return json.jsonify({
            'error': 'User already exists'
        }), 401

@app.route('/getUser', methods=['GET'])
def getuser():
    uid = request.args['uid']
    data = getUser(uid)
    if data:
        return json.jsonify({
            'data': data
        }), 200
    else:
        return json.jsonify({
            'error': 'Some error occured'
        }), 404

@app.route('/emit')
def emitt():
    socket.emit('socketRuns', {'data': 1245})
    return True

@socket.on('connect')
def test_connect():
    print('connected')
    emit('my response', {'data': 'Connected'})

@socket.on('typingSend')
def test(message):
    print('hi', message)
    return 'works'

if __name__ == "__main__":
    socket.run(app)