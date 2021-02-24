import json

from atlassian import Jira

jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')

# expect issue key as input from Ajax response
with open('data/IssueQueryResults.json', 'w') as f:   
        f.write(json.dumps(jira.get_all_project_issues("AI4", 'key')))
        
        #jira.get_all_project_issues("AI4", 'issueLinks')
        
        # jira.search_issues('issue in allIssuesInEpic(AI4-88)')
        