var graphType = "A";

function switchGraphButtonName() {
	var currentText = document.getElementById("switchGraphs").innerHTML;
	
	$.getScript('scripts/main.js', function() {});
	$.getScript('scripts/styles.js', function() {});
	
		if(currentText === "Click to view Developer Cluster") {
		document.getElementById("switchGraphs").innerHTML="Click to view Issue Tree"; 
	}
	else{
		document.getElementById("switchGraphs").innerHTML="Click to view Developer Cluster"; 
	}
}