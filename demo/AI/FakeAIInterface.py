from fakeAI.py
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

suggestions = []

@app.route('/epicDecomposition', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        #do things to parse the json of results

        suggestions = doThings(request.get_json())
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')