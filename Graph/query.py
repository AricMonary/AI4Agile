import json

from atlassian import Jira

jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')

# expect issue key as input from Ajax response
with open('data/IssueQueryResults.json', 'w') as f:   
        f.write(json.dumps(jira.issue('AI4-97')))