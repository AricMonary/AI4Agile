/* function getIssueFromURLParameters() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

	var currentText = document.getElementById("switchGraphs").innerHTML;
	
	if(currentText === "Click to view Developer Cluster") {
		graphType = "A";
	}
	else{
		graphType = "B";
	}

	var graphToGrab = urlParams.get('issueKey') + graphType;
	
    return graphToGrab;
} */

$(function() {
    "use strict";

    function e(e, n) {
        for (var t = n.length, o = 0; t >= o; o++) {
            var s = n[o].title;
            if (s === e) return n[o]
        }
        return null
    }
	
    var n = "#cy",
        network = networks[Object.keys(networks)[0]],
        style = styles[0];
    $(n).cytoscape({
        layout: {
            name: 'tree',
            orientation: "topToBottom",
            depthSpace: 4,
            breadthSpace: 4,
            subtreeSpace: 4,
        },
        wheelSensitivity: 0.05,
        //autolock : true, //make nodes not moveable
        ready: function() {
            window.cy = this, 
                    cy.load(network.elements), console.log(network);
                    console.log(style);
                    var o = e("default", style);
                    null === o && (o = style), cy.style().fromJson(o.style).update()        
        }
    })
});