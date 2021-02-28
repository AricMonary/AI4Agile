import json

from atlassian import Jira
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

from EpicDecomposition import EpicDecomposition
from StoryOptimization import StoryOptimization
from TaskGeneration import TaskGeneration

app = Flask(__name__)
CORS(app)
jira = Jira(
    url='https://ai4agile.atlassian.net/',
    username='aric.monary@gmail.com',
    password='1DUcQzOBmyhq38npvuC41330')

# Listener to generate suggestions for Epic Decomposition
@app.route('/epicDecompositionCreateSuggestions', methods=['POST', 'OPTIONS'])
def epicDecompositionCreateSuggestions():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        issueJSON = request.get_json()
        inputForAI = getAndProcessDescription(issueJSON['issueKey'])

        if int(issueJSON['sliderValue']) > len(inputForAI):
            sliderValue = len(inputForAI)
        else:
            sliderValue = int(issueJSON['sliderValue'])

        if len(inputForAI) != 0:
            suggestions = EpicDecomposition(inputForAI, sliderValue)
        else:
            suggestions = []

        return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json', 'Access-Control-Allow-Origin': '*'}
    else:
        print("Invalid epicDecompositionCreateSuggestions request.")

# Listener to generate suggestions for Story Optimization
@app.route('/storyOptimizationCreateSuggestions', methods=['POST', 'OPTIONS'])
def storyOptimizationCreateSuggestions():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        issueJSON = request.get_json()
        inputForAI = getAndProcessDescription(issueJSON['issueKey'])
        sliderValue = int(issueJSON['sliderValue'])

        if len(inputForAI) > 1:
            suggestions = StoryOptimization(inputForAI, sliderValue)
        else:
            suggestions = []

        return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json', 'Access-Control-Allow-Origin': '*'}
    else:
        print("Invalid storyOptimizationCreateSuggestions request.")

# Listener to generate suggestions for Task Generation
@app.route('/taskGenerationCreateSuggestions', methods=['POST', 'OPTIONS'])
def taskGenerationCreateSuggestions():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        issueJSON = request.get_json()
        inputForAI = getAndProcessDescription(issueJSON['issueKey'])

        if len(inputForAI) > 1:
            suggestions = TaskGeneration(inputForAI)
        else:
            suggestions = inputForAI

        return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json', 'Access-Control-Allow-Origin': '*'}
    else:
        print("Invalid taskGenerationCreateSuggestions request.")

def getAndProcessDescription(issueKey):
    description = jira.issue_field_value(issueKey, 'description')
    if description == None:
        return []
    initialBrokenDescription = description.split('.')
    processedDescription = [x for x in initialBrokenDescription if x != ''] # Remove empty strings
    # Remove starting space
    for i in range(len(processedDescription)):
        if(processedDescription[i][0] == ' '):
            processedDescription[i] = processedDescription[i][1:]
        processedDescription[i] = str(processedDescription[i]) + '.'

    return processedDescription

# Listener to create selected suggestions for Epic Decomposition
@app.route('/epicDecompositionCreateIssues', methods=['POST', 'OPTIONS'])
def epicDecompositionCreateIssues():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        suggestionsJSON = request.get_json()
        createStoryFromEpic(suggestionsJSON)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        print("Invalid epicDecompositionCreateIssues request.")

# Listener to create selected suggestions for Story Optimization
@app.route('/storyOptimizationCreateIssues', methods=['POST', 'OPTIONS'])
def storyOptimizationCreateIssues():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        suggestionsJSON = request.get_json()
        createStoryFromStory(suggestionsJSON)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json', 'Access-Control-Allow-Origin': '*'}
    else:
        print("Invalid storyOptimizationCreateIssues request.")

# Listener to create selected suggestions for Task Generation
@app.route('/taskGenerationCreateIssues', methods=['POST', 'OPTIONS'])
def taskGenerationCreateIssues():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        suggestionsJSON = request.get_json()
        createTaskFromStory(suggestionsJSON)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        print("Invalid taskGenerationCreateIssues request.")

def createStoryFromEpic(suggestionsJSON):
    projectKey = suggestionsJSON['projectKey']
    parentIssueKey = suggestionsJSON['parentIssueKey']
    parentFields = jira.issue(parentIssueKey)['fields']

    for suggestion in suggestionsJSON['suggestions']:
        fields = {
            'project': {'key': projectKey},
            'issuetype': {"name": "Story"},
            'parent': {'key': parentIssueKey},
            'summary': createSummaryFromDescription(suggestion),
            'description': suggestion,
        }
        if parentFields['reporter'] != None:
            fields['reporter'] = {'id': parentFields['reporter']['accountId']}
        if parentFields['assignee'] != None:
            fields['assignee'] = {'id': parentFields['assignee']['accountId']}
        # start date
        if parentFields['customfield_10015'] != None:
            fields['customfield_10015'] = parentFields['customfield_10015']
        if parentFields['duedate'] != None:
            fields['duedate'] = parentFields['duedate']
        if list(parentFields['labels']) != []:
            fields['labels'] = list(parentFields['labels'])

        newIssue = jira.issue_create(fields=fields)
        newIssueKey = newIssue['key']

        issueFields = {
            "type": {"name": "Blocks"},
            "inwardIssue": {"key": newIssueKey},
            "outwardIssue": {"key": parentIssueKey},
            "comment": {}
        }

        jira.create_issue_link(issueFields)

def createStoryFromStory(suggestionsJSON):
    projectKey = suggestionsJSON['projectKey']
    parentIssueKey = suggestionsJSON['parentIssueKey']
    parentEpicKey = (jira.issue_field_value(parentIssueKey, "parent"))['key']
    parentFields = jira.issue(parentIssueKey)['fields']

    for suggestion in suggestionsJSON['suggestions']:
        fields = {
            'project': {'key': projectKey},
            'issuetype': {"name": "Story"},
            'parent': {'key': parentEpicKey},
            'summary': createSummaryFromDescription(suggestion),
            'description': suggestion,
        }
        if parentFields['reporter'] != None:
            fields['reporter'] = {'id': parentFields['reporter']['accountId']}
        if parentFields['assignee'] != None:
            fields['assignee'] = {'id': parentFields['assignee']['accountId']}
        # start date
        if parentFields['customfield_10015'] != None:
            fields['customfield_10015'] = parentFields['customfield_10015']
        if parentFields['duedate'] != None:
            fields['duedate'] = parentFields['duedate']
        if list(parentFields['labels']) != []:
            fields['labels'] = list(parentFields['labels'])
        if parentFields['customfield_10020'] != None:
            fields['customfield_10020'] = parentFields['customfield_10020'][0]['id']

        jira.issue_create(fields=fields)

    # Add "Opimized" label to existing story that was optimzed
    labelFields = list((jira.issue_field_value(parentIssueKey, "labels")))
    labelFields.append('Optimized')

    labelFields = {'labels': labelFields}

    jira.update_issue_field(parentIssueKey, labelFields)

def createTaskFromStory(suggestionsJSON):
    projectKey = suggestionsJSON['projectKey']
    parentIssueKey = suggestionsJSON['parentIssueKey']
    parentEpicKey = (jira.issue_field_value(parentIssueKey, "parent"))['key']
    parentFields = jira.issue(parentIssueKey)['fields']

    for suggestion in suggestionsJSON['suggestions']:
        fields = {
            'project': {'key': projectKey},
            'issuetype': {"name": "Task"},
            'parent': {'key': parentEpicKey},
            'summary': createSummaryFromDescription(suggestion),
            'description': suggestion,
        }
        if parentFields['reporter'] != None:
            fields['reporter'] = {'id': parentFields['reporter']['accountId']}
        if parentFields['assignee'] != None:
            fields['assignee'] = {'id': parentFields['assignee']['accountId']}
        # start date
        if parentFields['customfield_10015'] != None:
            fields['customfield_10015'] = parentFields['customfield_10015']
        if parentFields['duedate'] != None:
            fields['duedate'] = parentFields['duedate']
        if list(parentFields['labels']) != []:
            fields['labels'] = list(parentFields['labels'])
        if parentFields['customfield_10020'] != None:
            fields['customfield_10020'] = parentFields['customfield_10020'][0]['id']

        newIssue = jira.issue_create(fields=fields)
        newIssueKey = newIssue['key']

        issueFields = {
            "type": {"name": "Blocks"},
            "inwardIssue": {"key": newIssueKey},
            "outwardIssue": {"key": parentIssueKey},
            "comment": {}
        }

        jira.create_issue_link(issueFields)

def createSummaryFromDescription(description):
    descriptionList = description.split('.')
    
    summary = ''
    for sentence in descriptionList:
        if len(summary) + len(sentence + '. ') < 254 and sentence != '' and sentence != ' ':
            summary += sentence + '. '
        else:
            return summary
    return summary

# Source: https://stackoverflow.com/a/52875875
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == '__main__':
    app.run()