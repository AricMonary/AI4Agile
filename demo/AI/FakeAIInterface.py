#from fakeAI import akeAI1DoingThings
import json
from atlassian import Jira
from flask import Flask, request

app = Flask(__name__)
jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')


@app.route('/fakeAI1', methods=['POST'])
def fakeAI1():
    suggestionsJSON = request.get_json()
    for suggestion in suggestionsJSON['suggestions']:
        createStoryFromSuggestion(suggestion)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def createFieldsFromSuggestion(suggestion):
    fields = {
        'project': {'key': 'AI4'},
        'issuetype': {"name": "Story"},
        'parent': {'key': 'AI4-107'},
        'summary': suggestion,
        'description': suggestion,
    }

    return fields


def createStoryFromSuggestion(suggestion):
    fields = createFieldsFromSuggestion(suggestion)
    jira.issue_create(fields=fields)


if __name__ == '__main__':
    app.run()