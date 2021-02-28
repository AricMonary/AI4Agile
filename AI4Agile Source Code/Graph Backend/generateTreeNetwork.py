import json
import re

from atlassian import Jira

jira = Jira(
    url='https://playingabout.atlassian.net/',
    username='aric.monary@wsu.edu',
    password='NCx7f7ZWle5yfwS3DB8JBCEA')

def generate_tree_dataset(issueKey):
    # expect issue key as input from Ajax response
    # with open('data/IssueQueryResults.json', 'w') as f:
    #        f.write(json.dumps(jira.issue('AI4-97')))

    nodes = []
    edges = []

    # Main source: https://isquared.digital/blog/2020-03-24-viz-tools-pt2-2/
    # with open('data/IssueQueryResults.json', 'r') as f:
    issueData = jira.issue(issueKey)  # json.load(f)  # setup issueData dictionary

    # Get project website for hrefs
    link = issueData.get("fields").get("project").get("self")
    link = link.partition("rest")[0]  # remove rest api parts
    link = link + "browse/"

    # Setup primary node to connect to
    selectedNode = {
        "data": {
            "id": str(1),  # the string representation of the unique node ID
            "idInt": 1,  # the numeric representation of the unique node ID
            "name": issueData.get("key"), # the name of the node used for printing
            "href": link + issueData.get("key"),  # web link for this issue
            "type": issueData.get("fields").get("issuetype").get("name") # issue type (Epic/Story/Task)
            },
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected on the graph
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
    nodes.append(selectedNode)

    # Get parent, if applicable
    if "parent" in issueData.get("fields"):
        name = str(issueData.get("fields").get("parent").get("key"))
        node = {
            "data": {
                # the string representation of the unique node ID
                "id": str(0),
                "idInt": 0,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name,  # web link for this issue
                "type": issueData.get("fields").get("parent").get("fields").get("issuetype").get("name") # issue type (Epic/Story/Task)
                },
                "group": "nodes",  # it belongs in the group of nodes
                "removed": False,
                "selected": False,  # the node is not selected on the graph
                "selectable": True,  # we can select the node
                "locked": False,  # the node position is not immutable
                "grabbable": True  # we can grab and move the node
            }
        nodes.append(node)
        edge = {
            "data": {
                "source": str(0), # source node id (edge comes from this node)(parent issue)
                "target": str(1), # target node id (edge goes to this node)(selected issue)
                "id": "e" + str(1)  # e for edge
            },
            "group": "edges",  # it belongs in the group of edges
            "removed": False,
            "selected": False,  # the edge is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the edge position is not immutable
            "grabbable": True,  # we can grab and move the node
            "directed": True  # the edge is directed
        }
        edges.append(edge)

    # Loop to get linked/blocking issues
    # issuelinks is a list of dictionaries, not a single dictionary
    issueLinks = issueData.get("fields").get("issuelinks")
    for i in range(0, len(issueLinks)):
        data = {}
        if issueLinks[i].get("inwardIssue") != None:
            # source node id (edge comes from this node)(current blocking issue)
            # target node id (edge goes to this node)(selected issue)
            # not matching -> returns None
            isPassive = re.search("is [a-z]+ by", issueLinks[i].get("type").get("inward"))
            data = {"source": "1", "target": str(i + 2), "id": "e" + str(i + 2)} if isPassive else {"source": str(i + 2), "target": "1", "id": "e" + str(i + 2)}
        
            name = (issueLinks[i]).get("inwardIssue").get("key")
            type = (issueLinks[i]).get("inwardIssue").get("fields").get("issuetype").get("name")
        elif (issueLinks[i]).get("outwardIssue") != None:
            data = {"source": str(i + 2), "target": "1", "id": "e" + str(i + 2)} # this issue blocks another "outward" issue
            name = (issueLinks[i]).get("outwardIssue").get("key")
            type = (issueLinks[i]).get("outwardIssue").get("fields").get("issuetype").get("name")
        else:
            continue

        node = {
            "data": {
                "id": str(i + 2), # the string representation of the unique node ID
                "idInt": i + 2,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name,
                "type": type  # issue type (Epic/Story/Task)
            },
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        edges.append(edge)

    networks = []
    networks.extend(nodes)
    networks.extend(edges)
    return json.dumps(networks)

    # with open('data/treeNetwork.js', 'w') as f2:  # create file in directory above
    #    filestart = "var treeNetwork = "
    #    f2.write(filestart)
    # with open('data/treeNetwork.js', 'a') as f2:
    #    f2.write(json.dumps(networks)) # add formatted nodes and edges to networks file
