function getIssueFromURLParameters() {
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
}

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
        network = networks[getIssueFromURLParameters()],
        style = styles[0];
    $(n).cytoscape({
        layout: {
            name: "preset",
            padding: 10, //space on edges when graph loads
            avoidOverlap: true,
            avoidOverlapPadding: 5,
            //fit: true, // fits to viewport, in theory
            //spacingFactor: 1.90
        },
        wheelSensitivity: 0.05,
        autolock : true, //make nodes not moveable
        //boxSelectionEnabled: !0,
        ready: function() {
            window.cy = this, 
                    cy.load(network.elements), console.log(network);
                    console.log(style);
                    var o = e("default", style);
                    null === o && (o = style), cy.style().fromJson(o.style).update()        
        }
    })
});