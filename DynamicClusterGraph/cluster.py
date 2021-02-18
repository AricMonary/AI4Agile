import json

from jira import JIRA

my_parent = 'AI4-88'


# Return the parent of the target issue
def get_epic(target_issue):
    # Authenticate JIRA
    auth_jira = JIRA(server='https://playingabout.atlassian.net/',
                     basic_auth=('phong.bach@wsu.edu', 'OOCqwKugtQBVE6sdFied7862'))

    # Get the issue
    current_issue = auth_jira.search_issues('issue = "' + target_issue + '"')

    return current_issue[0].fields.parent.key


# Generate JSON file network
def generate_dataset(target_parent):
    # Authenticate JIRA
    auth_jira = JIRA(server='https://playingabout.atlassian.net/',
                     basic_auth=('phong.bach@wsu.edu', 'OOCqwKugtQBVE6sdFied7862'))

    # Get all issues
    # current_issues = auth_jira.search_issues('parent = "' + target_parent + '"')

    current_epic = auth_jira.search_issues('project = AI4 AND issuetype = epic')
    current_story = auth_jira.search_issues('project = AI4 AND issuetype = story')
    current_task = auth_jira.search_issues('project = AI4 AND issuetype = task')
    current_issues = []
    current_issues.extend(current_epic)
    current_issues.extend(current_story)
    current_issues.extend(current_task)

    # Find the assignee for the issue
    # Map assignee to the issue
    assignee_set = set()
    assignee_and_issue_list = []

    # The dictionary is used to map the assignee and issue to the corresponding id
    assignee_and_issue_dict = {}

    for issue in current_issues:
        key = issue
        assignee = str(issue.fields.assignee)

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
        assignee_and_issue_dict[item.key] = i + 1
        node = {
            "data": {
                "id": str(i + 1),  # the string representation of the unique node ID
                "idInt": i + 1,  # the numeric representation of the unique node ID
                "name": item.key,
                "query": True
            },
            "classes": ["issue", item.fields.issuetype.name],  # the keyword 'classes' is used to group the nodes in classes
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)
        i = i + 1
    print(nodes)

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

    print(edges)

    # Calculate the indegree
    # initial dictionary mapping each node id to its normalized indegree
    NUM_NODES = len(assignee_set) + len(current_issues)
    nodes_indegree = dict(zip(list(range(1, NUM_NODES + 1)), [0] * (NUM_NODES + 1)))
    N = len(edges)
    for e in edges:
        nodes_indegree[int(e["data"]["target"])] += 1.0 / N

    print(max(list(nodes_indegree.values())))

    for node in nodes:
        node["data"]["score"] = nodes_indegree[node["data"]["idInt"]]

    # Write the data in a JSON file
    data = []
    data.extend(nodes)
    data.extend(edges)

    with open('datasets/custom.json', 'w') as f:
        json.dump(data, f)


# Main
generate_dataset(my_parent)
