var clusterNetwork = [];
var treeNetwork = [];

function getAndRenderGraphs() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var setOfIssueKey = {};
    setOfIssueKey['issueKey'] = urlParams.get('parentIssueKey');
    setOfIssueKey['projectKey'] = urlParams.get('projectKey');
    var jsonOfIssueKey = JSON.stringify(setOfIssueKey);

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/clusterGraphGenerateNetwork",
        async: false,
        data: jsonOfIssueKey,
        contentType: "application/json",
        success: function (data) {
            replyData = JSON.parse(data);
            console.log(replyData);
            clusterNetwork = replyData['clusterNetwork'];
            console.log(clusterNetwork);
        }
    });

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/treeGraphGenerateNetwork",
        async: false,
        data: jsonOfIssueKey,
        contentType: "application/json",
        success: function (data) {
            replyData = JSON.parse(data);
            console.log(replyData);
            treeNetwork = replyData['treeNetwork'];
            console.log(treeNetwork);
        }
    });

    console.log(treeNetwork);
    console.log(clusterNetwork);

    var cyTr = cytoscape({
        container: document.getElementById('cyTr'),
        elements: treeNetwork,
        layout: treeLayout,
        style: treeStyle,
        zoomingEnabled: true
    });
    var cyCl = cytoscape({
        container: document.getElementById('cyCl'),
        elements: clusterNetwork,
        layout: clusterLayout,
        style: clusterStyle,
        zoomingEnabled: true
    });
    $(document).ready(function () {
        // Open the "href" node attribute on click
        cyTr.on('tap', 'node', function () {
            try { // browser may block popups
                window.open(this.data('href'));
            } catch (e) { // fall back on url change
                window.location.href = this.data('href');
            }
        });
    });
    $(window).ready(function () {
        cyTr.on('resize', function (event) {
            cyTr.center();
            cyTr.fit();
        });
        cyCl.on('resize', function (event) {
            cyCl.center();
            cyCl.fit();
        });
    });
}
