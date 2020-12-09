import json

from atlassian import Jira
from flask import Flask, request

from EpicDecomposition import *
from StoryOptimization import *
from TaskGeneration import *

app = Flask(__name__)
jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')

# Listener to generate suggestions for Epic Decomposition
@app.route('/epicDecompositionCreateSuggestions', methods=['POST'])
def epicDecompositionCreateSuggestions():
    issueJSON = request.get_json()
    inputForAI = getAndProcessDescription(issueJSON['issueKey'])
    sliderValue = issueJSON['sliderValue']

    suggestions = EpicDecomposition(inputForAI, sliderValue)

    return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json'}

# Listener to generate suggestions for Story Optimization
@app.route('/storyOptimizationCreateSuggestions', methods=['POST'])
def storyOptimizationCreateSuggestions():
    issueJSON = request.get_json()
    inputForAI = getAndProcessDescription(issueJSON['issueKey'])
    sliderValue = int(issueJSON['sliderValue'])

    suggestions = StoryOptimization(inputForAI, sliderValue)

    return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json'}

# Listener to generate suggestions for Task Generation
@app.route('/taskGenerationCreateSuggestions', methods=['POST'])
def taskGenerationCreateSuggestions():
    issueJSON = request.get_json()
    inputForAI = getAndProcessDescription(issueJSON['issueKey'])

    suggestions = TaskGeneration(inputForAI)

    return json.dumps({'success': True, 'suggestions': suggestions}), 200, {'ContentType': 'application/json'}

def getAndProcessDescription(issueKey):
    description = jira.issue_field_value(issueKey, 'description')
    initialBrokenDescription = description.split('.')
    processedDescription = [x for x in initialBrokenDescription if x != ''] # Remove empty strings
    # Remove starting space
    for i in range(len(processedDescription)):
        if(processedDescription[i][0] == ' '):
            processedDescription[i] = processedDescription[i][1:]
        processedDescription[i] = str(processedDescription[i]) + '.'

    return processedDescription

# Listener to create selected suggestions for Epic Decomposition
@app.route('/epicDecompositionCreateIssues', methods=['POST'])
def epicDecompositionCreateIssues():
    suggestionsJSON = request.get_json()

    createStoryFromEpic(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# Listener to create selected suggestions for Story Optimization
@app.route('/storyOptimizationCreateIssues', methods=['POST'])
def storyOptimizationCreateIssues():
    suggestionsJSON = request.get_json()
    createStoryFromStory(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# Listener to create selected suggestions for Task Generation
@app.route('/taskGenerationCreateIssues', methods=['POST'])
def taskGenerationCreateIssues():
    suggestionsJSON = request.get_json()

    createTaskFromStory(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def createStoryFromEpic(suggestionsJSON):
    projectKey = suggestionsJSON['projectKey']
    parentIssueKey = suggestionsJSON['parentIssueKey']
    parentFields = jira.issue(parentIssueKey)['fields']

    for suggestion in suggestionsJSON['suggestions']:
        fields = {
            'project': {'key': projectKey},
            'issuetype': {"name": "Story"},
            'parent': {'key': parentIssueKey},
            'summary': suggestion,
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

        jira.issue_create(fields=fields)

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
            'summary': suggestion,
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
            'summary': suggestion,
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

if __name__ == '__main__':
    app.run()
