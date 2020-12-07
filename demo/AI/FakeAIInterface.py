import json
from atlassian import Jira
from flask import Flask, request

app = Flask(__name__)
jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')

# Listener to POST requests for the 
@app.route('/epicDecomposition', methods=['POST'])
def epicDecomposition():
    suggestionsJSON = request.get_json()

    createStoryFromEpic(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/storyOptimization', methods=['POST'])
def storyOptimization():
    suggestionsJSON = request.get_json()
    createStoryFromStory(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/taskGeneration', methods=['POST'])
def taskGeneration():
    suggestionsJSON = request.get_json()

    createTaskFromStory(suggestionsJSON)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

def createStoryFromEpic(suggestionsJSON):
    projectKey = suggestionsJSON['projectKey']
    parentIssueKey = suggestionsJSON['parentIssueKey']
    for suggestion in suggestionsJSON['suggestions']:
        fields = {
            'project': {'key': projectKey},
            'issuetype': {"name": "Story"},
            'parent': {'key': parentIssueKey},
            'summary': suggestion,
            'description': suggestion,
        }
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
            'reporter': {'id': parentFields['reporter']['accountId']},
            'assignee': {'id': parentFields['assignee']['accountId']},
            'customfield_10015': parentFields['customfield_10015'], # Start date
            'duedate': parentFields['duedate'],
            'labels': list(filter(lambda x: x != 'Optimized', list(parentFields['labels']))),
            'customfield_10020': parentFields['customfield_10020'][0]['id'], # Sprint
        }

        jira.issue_create(fields=fields)
    
    #Add "Opimized" label to existing story that was optimzed
    labelFields = list((jira.issue_field_value(parentIssueKey, "labels")))
    labelFields.append('Optimized')

    labelFields = {'labels': labelFields}

    #print(labelFields)

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
            'reporter': {'id': parentFields['reporter']['accountId']},
            'assignee': {'id': parentFields['assignee']['accountId']},
            'customfield_10015': parentFields['customfield_10015'], # Start date
            'duedate': parentFields['duedate'],
            'labels': list(filter(lambda x: x != 'Optimized', list(parentFields['labels']))), # filters out the 'Optimized' label
            'customfield_10020': parentFields['customfield_10020'][0]['id'], # Sprint
        }

        newIssue = jira.issue_create(fields=fields)
        newIssueKey = newIssue['key']

        issueFields = {
            "type": {"name": "Blocks" },
            "inwardIssue": { "key": newIssueKey},
            "outwardIssue": {"key": parentIssueKey},
            "comment": {}
        }

        jira.create_issue_link(issueFields)

if __name__ == '__main__':
    app.run()