function switchGraph() {
	var currentText = document.getElementById("switchGraphs").innerHTML;
		
	if (currentText === "View Developer Cluster") {
		document.getElementById("switchGraphs").innerHTML="View Issue Tree";
		document.getElementById("cyTr").setAttribute('style', 'display: none;')
		document.getElementById("cyCl").setAttribute('style', 'display: block')
	}
	else {
		document.getElementById("switchGraphs").innerHTML="View Developer Cluster"; 
		document.getElementById("cyTr").setAttribute('style', 'display: block')
		document.getElementById("cyCl").setAttribute('style', 'display: none;')
	}
}
