import json

nodes = []

# Main source: https://isquared.digital/blog/2020-03-24-viz-tools-pt2-2/
with open('IssueQueryResults.json') as f:
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
            "href": link + issueData.get("key")
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
                "href": link + name
            },
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected on the graph
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)

    # Loop to get linked/blocking issues
    issueLinks = issueData.get("fields").get("issuelinks") # issuelinks is a list of dictionaries, not a single dictionary
    for i in range(0, len(issueLinks)):
        name = (issueLinks[i]).get("inwardIssue").get("key")
        node = {
            "data": {
                "id": str(i + 2),  # the string representation of the unique node ID
                "idInt": i + 2,  # the numeric representation of the unique node ID
                "name": name,  # the name of the node used for printing
                "href": link + name
            },
            "group": "nodes",  # it belongs in the group of nodes
            "removed": False,
            "selected": False,  # the node is not selected
            "selectable": True,  # we can select the node
            "locked": False,  # the node position is not immutable
            "grabbable": True  # we can grab and move the node
        }
        nodes.append(node)
print(nodes)