from flask import Flask
from flask import request, make_response, jsonify
import base64
import csv
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('data.csv') as data:
        reader = csv.reader(data)
        for row in reader:
            if(row[0]==request.args.get('name')):
                print(json.loads(row[2])[0].encode('utf-8').strip())
                file1 = open(json.loads(row[2])[0].encode('utf-8').strip(), 'rb').read()
                image = base64.b64encode(file1).decode('utf')
                response = jsonify([row[0],row[1],image])
                response.headers.add('Access-Control-Allow-Origin', 'null')
                return response