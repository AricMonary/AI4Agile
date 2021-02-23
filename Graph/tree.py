import json

nodes = []
edges = []

# Main source: https://isquared.digital/blog/2020-03-24-viz-tools-pt2-2/
with open('data/IssueQueryResults.json', 'r') as f:
    issueData = json.load(f) # setup issueData dictionary

    # Get project website for hrefs
    link = issueData.get("fields").get("project").get("self")
    link = link.partition("rest")[0] # remove rest api parts
    link = link + "browse/"

    # Setup primary node to connect to
    selectedNode = {
        "data": {
            "id": str(1),  # the string representation of the unique node ID
            "idInt": 1,  # the numeric representation of the unique node ID
            "name": issueData.get("key"),  # the name of the node used for printing
            "href": link + issueData.get("key"),
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
                "id": str(0),  # the string representation of the unique node ID
                "idInt": 0,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name,
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
                "source": str(1),  # the source node id (edge comes from this node)(selected issue)
                "target": str(0),  # the target node id (edge goes to this node)(parent issue)
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
    issueLinks = issueData.get("fields").get("issuelinks") # issuelinks is a list of dictionaries, not a single dictionary
    for i in range(0, len(issueLinks)):
        name = (issueLinks[i]).get("inwardIssue").get("key")
        node = {
            "data": {
                "id": str(i + 2),  # the string representation of the unique node ID
                "idInt": i + 2,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name,
                "type": (issueLinks[i]).get("inwardIssue").get("fields").get("issuetype").get("name") # issue type (Epic/Story/Task)
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
                "source": str(i + 2),  # the source node id (edge comes from this node)(current blocking issue)
                "target": str(1),  # the target node id (edge goes to this node)(selected issue)
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
    with open('data/network.js', 'w') as f2: # create file in directory above
        filestart = "var network = "
        f2.write(filestart)
    with open('data/network.js', 'a') as f2:   
        f2.write(json.dumps(networks))  # add formatted nodes and edges to networks file