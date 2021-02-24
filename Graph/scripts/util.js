var graphType = "tree";

function switchGraphButtonName() {
	var currentText = document.getElementById("switchGraphs").innerHTML;
	
	$.getScript('scripts/main.js', function() {});
	//$.getScript('styles/styles.json', function() {});
	
	if (currentText === "Click to view Developer Cluster") {
		document.getElementById("switchGraphs").innerHTML="Click to view Issue Tree"; 
	}
	else {
		document.getElementById("switchGraphs").innerHTML="Click to view Developer Cluster"; 
	}
}

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