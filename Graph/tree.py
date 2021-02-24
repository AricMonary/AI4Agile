import json

nodes = []
edges = []

# Main source: https://isquared.digital/blog/2020-03-24-viz-tools-pt2-2/
with open('data/IssueQueryResults.json', 'r') as f:
    issueData = json.load(f)  # setup issueData dictionary

    # Get project website for hrefs
    link = issueData.get("fields").get("project").get("self")
    link = link.partition("rest")[0]  # remove rest api parts
    link = link + "browse/"

    # Setup primary node to connect to
    selectedNode = {
        "data": {
            "id": str(1),  # the string representation of the unique node ID
            "idInt": 1,  # the numeric representation of the unique node ID
            # the name of the node used for printing
            "name": issueData.get("key"),
            "href": link + issueData.get("key"),
            # issue type (Epic/Story/Task)
            "type": issueData.get("fields").get("issuetype").get("name")
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
                "href": link + name,
                # issue type (Epic/Story/Task)
                "type": issueData.get("fields").get("parent").get("fields").get("issuetype").get("name")
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
                # the source node id (edge comes from this node)(selected issue)
                "source": str(1),
                # the target node id (edge goes to this node)(parent issue)
                "target": str(0),
                "id": "e" + str(1)
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

    # Loop to get linked/blocking issues
    # issuelinks is a list of dictionaries, not a single dictionary
    issueLinks = issueData.get("fields").get("issuelinks")
    for i in range(0, len(issueLinks)):
        if issueLinks[i].get("inwardIssue") != None:
            name = (issueLinks[i]).get("inwardIssue").get("key")
            type = (issueLinks[i]).get("inwardIssue").get("fields").get("issuetype").get("name")
        elif (issueLinks[i]).get("outwardIssue") != None:
            name = (issueLinks[i]).get("outwardIssue").get("key")
            type = (issueLinks[i]).get("outwardIssue").get("fields").get("issuetype").get("name")
        else:
            continue
        node = {
            "data": {
                # the string representation of the unique node ID
                "id": str(i + 2),
                "idInt": i + 2,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name,
                # issue type (Epic/Story/Task)
                "type": type
            },
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)
        edge = {
            "data": {
                # the source node id (edge comes from this node)(current blocking issue)
                "source": str(i + 2),
                # the target node id (edge goes to this node)(selected issue)
                "target": str(1),
                "id": "e" + str(i + 2)
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

    #els = {}
    #A = {}
    #networks = {}
    #els["nodes"] = nodes
    #els["edges"] = edges
    #A["elements"] = els
    #networks["A"] = A
    networks = []
    networks.extend(nodes)
    networks.extend(edges)
    with open('data/network.js', 'w') as f2:  # create file in directory above
        filestart = "var network = "
        f2.write(filestart)
    with open('data/network.js', 'a') as f2:
        # add formatted nodes and edges to networks file
        f2.write(json.dumps(networks))
