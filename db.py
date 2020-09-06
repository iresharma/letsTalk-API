import pymongo
from uuid import uuid4
import yaml

dbfile = open('creds.yaml', 'r')
dbdict = yaml.load(dbfile, Loader=yaml.FullLoader)
client = pymongo.MongoClient(dbdict['dbLink'])
userRef = client.Users
channelRef = client.Channels

def createToken():
    token = str(uuid4()).replace('-', '') + str(uuid4).replace('_', '')
    return token

def reassignToken(uid: str):
    userRef['tokens'].delete_many(
        {
            'uid': uid
        }
    )
    token = createToken()
    userRef['tokens'].insert_one(
        {
            'token': token,
            'uid': uid
        }
    )
    return token


def createUser(userData: dict):
    user = userRef['Users'].find_one({
        'email': userData['email']
    })
    if user == None:
        token = createToken()
        uid = str(uuid4()).replace('-', '')
        userRef['tokens'].insert_one(
            {
                'token': token,
                'uid': uid
            }
        )
        userRef['Users'].insert_one(
            {
                '_id': uid,
                'name': userData['name'],
                'email': userData['email'],
                'username': userData['username'],
                'password': userData['password']
            }
        )
        return uid, token
    else: return False

def checkToken(token: str):
    result = userRef['tokens'].find_one({
        'token': token
    })
    if result == None:
        return False
    else:
        return result['uid']

def getUser(uid: str):
    result = userRef['Users'].find_one(
        {
            '_id': uid
        }
    )
    if result == None:
        return False
    else:
        result['_id'] = str(result['_id'])
        return result


def emailLogin(email: str, password: str):
    result = userRef['Users'].find_one(
        {
            'email': email
        }
    )
    if result == None: return 'Not found'
    elif result['password'] != password: return False
    else: return result

def usernamelogin(username: str, password: str):
    result = userRef['Users'].find_one(
        {
            'username': username
        }
    )
    if result == None: return 'Not found'
    elif result['password'] != password: return False
    else: return result