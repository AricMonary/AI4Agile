var graphType = "tree";

function switchGraph() {
	var currentText = document.getElementById("switchGraphs").innerHTML;
	
	//$.getScript('styles/styles.json', function() {});
	
	if (currentText === "Click to view Developer Cluster") {
		document.getElementById("switchGraphs").innerHTML="Click to view Issue Tree";
		//loadClusterGraph() 
	}
	else {
		document.getElementById("switchGraphs").innerHTML="Click to view Developer Cluster"; 
		//loadTreeGraph()
	}
}

function loadTreeGraph() {
	/* cy.json({
		elements: treeNetwork, 
		style: treeStyle, 
		layout: treeLayout,
		zoomingEnabled: true
	}) */
}

function loadClusterGraph() {
	/* cy = document.getElementById('cy')
	cy.json({
		style: testStyle, 
		elements: testNetwork, 
		layout: clusterLayout, 
		style: treeStyle, //temp
		zoomingEnabled: true,
	}) */
}

/* function getIssueFromURLParameters() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

	var currentText = document.getElementById("switchGraphs").innerHTML;
	
	if(currentText === "Click to view Developer Cluster") {
		graphType = "tree";
	}
	else{
		graphType = "cluster";
	}

	var graphToGrab = urlParams.get('issueKey') + graphType;
	
    return graphToGrab;
} */