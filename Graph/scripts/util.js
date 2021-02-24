function switchGraph() {
	var currentText = document.getElementById("switchGraphs").innerHTML;
		
	if (currentText === "View Developer Cluster") {
		document.getElementById("switchGraphs").innerHTML="View Issue Tree";
		document.getElementById("cyTr").setAttribute('style', 'display: none;')
		document.getElementById("cyCl").setAttribute('style', 'display: inline')
	}
	else {
		document.getElementById("switchGraphs").innerHTML="View Developer Cluster"; 
		document.getElementById("cyTr").setAttribute('style', 'display: inline')
		document.getElementById("cyCl").setAttribute('style', 'display: none;')
	}
}
