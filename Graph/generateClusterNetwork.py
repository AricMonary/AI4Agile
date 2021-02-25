import json

from atlassian import Jira
from flask import Flask, request

# project = 'AI4'

app = Flask(__name__)

# Authenticate JIRA
jira = Jira(
    url="https://playingabout.atlassian.net/",
    username="phong.bach@wsu.edu",
    password="OOCqwKugtQBVE6sdFied7862",
)

# Listener to generate network for cluster graph
@app.route('/clusterGraphGenerateNetwork', methods=['POST'])
def clusterGraphGenerateNetwork():
    issueJSON = request.get_json()
    
    # Get issue key
    issueKey = issueJSON['issueKey']
    index = issueKey.index('-')

    # Get project name
    projectID = issueKey[0:index]
    clusterNetwork = generate_dataset(projectID)

    return json.dumps({'success': True, 'clusterNetwork': clusterNetwork}), 200, {'ContentType': 'application/json'}


# Generate network file in javascript
def generate_dataset(project):
    # Get all issues
    query = 'project = ' + project + ' AND (issuetype = "epic" OR issuetype = "story" OR issuetype = "task")'
    current_issues = jira.jql(query, limit=1000)

    current_issues = current_issues['issues']

    # Find the assignee for the issue
    # Map assignee to the issue
    assignee_set = set()
    assignee_and_issue_list = []

    # The dictionary is used to map the assignee and issue to the corresponding id
    assignee_and_issue_dict = {}

    for issue in current_issues:
        key = issue["key"]

        if issue["fields"]["assignee"] is None:
            assignee = "None"
        else:
            assignee = str(issue["fields"]["assignee"]["displayName"])

        words = assignee.split(" ")
        letters = [word[0] for word in words]
        assignee_initial = "".join(letters)

        # Add assignee to the list
        assignee_set.add(assignee_initial)

        # Add assignee and issue tuple to the list
        assignee_and_issue_list.append((assignee_initial, key))

    # Generate the nodes
    nodes = []  # the final subset of nodes
    packages = []  # the set of packages for each node

    i = 0
    for item in assignee_set:
        assignee_and_issue_dict[item] = i + 1
        node = {
            "data": {
                "id": str(i + 1),  # the string representation of the unique node ID
                "idInt": i + 1,  # the numeric representation of the unique node ID
                "name": item,
                "query": True
            },
            "classes": "assignee",  # the keyword 'classes' is used to group the nodes in classes
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)
        i = i + 1

    for item in current_issues:
        assignee_and_issue_dict[item["key"]] = i + 1
        node = {
            "data": {
                "id": str(i + 1),  # the string representation of the unique node ID
                "idInt": i + 1,  # the numeric representation of the unique node ID
                "name": item["key"],
                "query": True
            },
            "classes": ["issue", item["fields"]["issuetype"]["name"]],
            # the keyword 'classes' is used to group the nodes in classes
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)
        i = i + 1

    # Get the edges
    # get the source node and the target node
    edges = []
    i = 2

    for item in assignee_and_issue_list:
        source, target = item[0], item[1]

        # Get the correct id for the source and target
        source_ID = assignee_and_issue_dict[str(source)]
        target_ID = assignee_and_issue_dict[str(target)]

        edge = {
            "data": {
                "source": source_ID,  # the source node id (edge comes from this node)
                "target": target_ID,  # the target node id (edge goes to this node)
                "directed": True,
                "intn": True,
                "rIntnId": i - 1,
                "id": "e" + str(i - 1)
            },
            "position": {},  # the initial position is not known
            "group": "edges",  # it belongs in the group of edges
            "removed": False,
            "selected": False,  # the edge is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the edge position is not immutable
            "grabbable": True,  # we can grab and move the node
            "directed": True  # the edge is directed
        }
        edges.append(edge)
        i = i + 1

    # Calculate the indegree
    # initial dictionary mapping each node id to its normalized indegree
    NUM_NODES = len(assignee_set) + len(current_issues)
    nodes_indegree = dict(zip(list(range(1, NUM_NODES + 1)), [0] * (NUM_NODES + 1)))
    N = len(edges)
    for e in edges:
        nodes_indegree[int(e["data"]["target"])] += 1.0 / N

    for node in nodes:
        node["data"]["score"] = nodes_indegree[node["data"]["idInt"]]

    # Write the data in a JSON file
    data = []
    data.extend(nodes)
    data.extend(edges)

    return json.dumps(data)
    # with open('network.js', 'w') as f:
    #     f.write('var network = ')
    #     json.dump(data, f)


# Main
generate_dataset(project)