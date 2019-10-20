from flask import Flask
from flask import request, make_response, jsonify
import base64
import csv
import json
from flask_cors import CORS
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()+'/Training_Data/'

CORS(app)

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
                # response.headers.add('Access-Control-Allow-Origin', 'null')
                return response

@app.route('/new',methods=["POST"])
def new_image():
    # print(request.files.getlist("file"))
    name = request.form["name"]
    description = request.form["description"]
    file_paths = []
    for file in request.files.getlist("file"):
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], name)):
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], name))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name + '/' +file.filename))
        file_paths.append(os.path.join(app.config['UPLOAD_FOLDER'], name + '/' +file.filename))
    
    fields=[name, description,json.dumps(file_paths)]
    print(fields)
    # print(json.loads(request.data.decode('utf')))
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return "request.data"
