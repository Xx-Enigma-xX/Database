from flask import Flask
from flask import request
app = Flask(__name__)

from flask import jsonify, make_response
import time
import sys
import config

import os
import shutil

sys.path.insert(0, '..')
from database import Database

@app.route('/')
def status():
    try:
        if request.headers['token'] == config.token:
            authorized = True
        else:
            raise Exception("Incorrect token.")
    except:
        authorized = False
    if authorized:
        uptime = time.time() - startTime
        response = {'type': 'Enigma Database', 'version': '2.0',
        'uptime': uptime, 'error': None}
        statusCode = 200
    else:
        response = {'type': 'Enigma Database', 'version': '???',
        'uptime': '???', 'error': 'Unauthorized'}
        statusCode = 401
    return make_response(jsonify(response), statusCode)

@app.route('/<databaseName>/<databaseContainer>')
def vars():
    try:
        if request.headers['token'] == config.token:
            authorized = True
        else:
            raise Exception("Incorrect token.")
    except:
        authorized = False
    if authorized:
        uptime = time.time() - startTime
        response = {'type': 'Enigma Database', 'version': '2.0',
        'uptime': uptime, 'error': None}
        statusCode = 200
    else:
        response = {'type': 'Enigma Database', 'version': '???',
        'uptime': '???', 'error': 'Unauthorized'}
        statusCode = 401
    return make_response(jsonify(response), statusCode)

if __name__ == "__main__":
    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('crts/public.crt', "crts/private.key")

    startTime = time.time()
    app.run(host=config.url, port=config.port, ssl_context=context)
