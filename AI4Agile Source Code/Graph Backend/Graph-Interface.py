import json
from flask import Flask, request, make_response
from generateClusterNetwork import generate_cluster_dataset
from generateTreeNetwork import generate_tree_dataset
from flask_cors import CORS

# project = 'AI4'

app = Flask(__name__)
CORS(app)

# Listener to generate network for cluster graph
@app.route('/clusterGraphGenerateNetwork', methods=['POST', 'OPTIONS'])
def clusterGraphGenerateNetwork():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        issueJSON = request.get_json()
        # Get project name
        projectID = issueJSON['projectKey']

        clusterNetwork = generate_cluster_dataset(projectID)

        return json.dumps({'success': True, 'clusterNetwork': clusterNetwork}), 200, {'ContentType': 'application/json'}

# Listener to generate network for tree graph
@app.route('/treeGraphGenerateNetwork', methods=['POST', 'OPTIONS'])
def treeGraphGenerateNetwork():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        issueJSON = request.get_json()
        # Get issue key
        issueKey = issueJSON['issueKey']
        
        treeNetwork = generate_tree_dataset(issueKey)

        return json.dumps({'success': True, 'treeNetwork': treeNetwork}), 200, {'ContentType': 'application/json'}

# Source: https://stackoverflow.com/a/52875875
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == '__main__':
    app.run()