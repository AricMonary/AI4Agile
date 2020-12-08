var suggestionsCreated = false;
var suggestionCount = 0;
var suggestions = []
var paramtersFromURL = {}

function loadsuggestions() {
    parametersFromURL = getURLParameters();
    
    processType = parametersFromURL['processType'];
    issueKey = parametersFromURL['parentIssueKey'];

    suggestions = generateSuggestions(processType, issueKey);

    renderSuggestions();
}

function generateSuggestions(processType, issueKey) {
    var jsonOfIssueKey = JSON.stringify({ 'issueKey': issueKey })

    suggestions = []

    switch (processType) {
        //for the epic decomposition process
        case 'epicDecomposition':

            console.log("Epic Decomposition Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/epicDecompositionCreateSuggestions", //localhost Flask
                data: jsonOfIssueKey,
                contentType: "application/json",
                success:function(data) {
                    suggestions = data['suggestions']; 
                  }
            });
            break;

        //for the story optimization process
        case 'storyOptimization':

            console.log("Story Optimization Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/storyOptimizationCreateSuggestions",
                data: jsonOfIssueKey,
                contentType: "application/json",
                success:function(data) {
                    suggestions = data; 
                  }
            });
            break;

        //for the task generation process
        case 'taskGeneration':

            console.log("Task Generation Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/taskGenerationCreateSuggestions",
                data: jsonOfIssueKey,
                contentType: "application/json",
                success:function(data) {
                    suggestions = data;  
                  }
            });
            break;
    }

    return suggestions;
}

function renderSuggestions() {
    if (!(document.getElementById('createSuggestions').disabled)) {

        var div = document.getElementById('suggestions');
        for (suggestion of suggestions) {
            var newDiv = document.createElement("div");
            newDiv.setAttribute("class", "suggestion")
            // create the necessary elements
            var label = document.createElement("label");
            label.setAttribute("contenteditable", "true");
            label.setAttribute("for", "suggestion");
            label.setAttribute('onChange', 'suggestionDeleted(this)');
            label.appendChild(document.createTextNode(suggestion));

            var checkbox = document.createElement("input");
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('name', 'suggestion');
            //checkbox.setAttribute('checked', 'true');

            // add the label element to your div
            newDiv.appendChild(checkbox);
            newDiv.appendChild(label);
            newDiv.appendChild(document.createElement("br"));
            div.appendChild(newDiv);
        }
    }

    document.getElementById('selectAll').disabled = false;
    document.getElementById('deselectAll').disabled = false;
    document.getElementById('createSuggestions').disabled = true;
}

// For demo button
function createSuggestions() {
    if (!(document.getElementById('createSuggestions').disabled)) {
        var suggestions = ["suggestion 1", "suggestion 2", "suggestion 3", "a very very very very very very very very very very very long suggestion", "...", "suggestion x"]; //query script here

        var div = document.getElementById('suggestions');
        for (suggestion of suggestions) {
            var newDiv = document.createElement("div");
            newDiv.setAttribute("class", "suggestion")
            // create the necessary elements
            var label = document.createElement("label");
            label.setAttribute("contenteditable", "true");
            label.setAttribute("for", "suggestion");
            label.setAttribute('onChange', 'suggestionDeleted(this)');
            label.appendChild(document.createTextNode(suggestion));

            var checkbox = document.createElement("input");
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('name', 'suggestion');
            //checkbox.setAttribute('checked', 'true');

            // add the label element to your div
            newDiv.appendChild(checkbox);
            newDiv.appendChild(label);
            newDiv.appendChild(document.createElement("br"));
            div.appendChild(newDiv);
        }
    }

    document.getElementById('selectAll').disabled = false;
    document.getElementById('deselectAll').disabled = false;
    document.getElementById('createSuggestions').disabled = true;
}

function checkAllSuggestions(checked) {
    var checkboxes = document.getElementsByName('suggestion');
    for (checkbox of checkboxes) {
        checkbox.checked = checked;
    }
}

function selectAll() {
    checkAllSuggestions(true);
}

function deselectAll() {
    checkAllSuggestions(false);
}

function createSelectedSuggestions() {
    var populatedSuggestions = document.getElementsByName('suggestion');
    var checkedSuggestions = new Array();
    for (i = 0; i < populatedSuggestions.length; i++) {
        if (populatedSuggestions[i].checked == true) {
            checkedSuggestions.push(populatedSuggestions[i].parentElement.childNodes[1].innerHTML);
        }
    }

    var paramtersFromURL = getURLParameters();

    var processType = paramtersFromURL['processType'];

    var suggestionsToSend = {
        'projectKey': paramtersFromURL['projectKey'],
        'parentIssueKey': paramtersFromURL['parentIssueKey'],
        'suggestions': checkedSuggestions
    };

    //console.log("Process Type: " + processType)

    switch (processType) {
        //for the epic decomposition process
        case 'epicDecomposition':

            //console.log("Epic Decomposition Suggestion Creation: " + JSON.stringify(suggestionsToSend))

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/epicDecompositionCreateIssues", //localhost Flask
                data: JSON.stringify(suggestionsToSend),
                contentType: "application/json",
            });
            break;

        //for the story optimization process
        case 'storyOptimization':

            //console.log("Story Optimization Suggestion Creation: " + JSON.stringify(suggestionsToSend))

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/storyOptimizationCreateIssues",
                data: JSON.stringify(suggestionsToSend),
                contentType: "application/json",
            });
            break;

        //for the task generation process
        case 'taskGeneration':

            //console.log("Task Generation Suggestion Creation: " + JSON.stringify(suggestionsToSend))

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/taskGenerationCreateIssues",
                data: JSON.stringify(suggestionsToSend),
                contentType: "application/json",
            });
            break;
    }

    for (i = populatedSuggestions.length - 1; i >= 0; i--) {
        if (populatedSuggestions[i].checked == true) {
            suggestionDeleted(populatedSuggestions[i]);
        }
    }

    if (document.getElementById('suggestions').childElementCount == 0) {
        document.getElementById('selectAll').disabled = true;
        document.getElementById('deselectAll').disabled = true;
        document.getElementById('createSuggestions').disabled = false;
    }
    //CLOSE FIELD
}

function suggestionDeletedByClearingText(suggestion) {
    alert(suggestion.parentElement.childNodes[1].innerHTML)
    if (suggestion.childNodes[1].nodeValue == "") {
        document.getElementsByName('suggestions').removeChild(suggestion);
    }
}

function suggestionDeleted(suggestion) {
    suggestion.parentElement.remove();
}

function addSuggestion(suggestion) {
    var issues = document.getElementById("issues");
    issues.appendChild(document.createTextNode(suggestion.parentElement.childNodes[1].innerHTML));
    issues.appendChild(document.createElement("br"));
}

// Get the process type used (Epic Decomposition, Story Optimization, or Task Generation)
function getURLParameters() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var parameterSet = {};
    parameterSet['projectKey'] = urlParams.get('projectKey');
    parameterSet['parentIssueKey'] = urlParams.get('parentIssueKey');
    parameterSet['processType'] = urlParams.get('processType');

    return parameterSet;
}

range.addEventListener("input", () => {
    bubble.innerHTML = rangel.value;
});

function populateRange() {
    processType = getURLParameters()['processType'];

    // Loads the range for the Epic Decomposition Process
    if (processType == 'epicDecomposition') {
        var div = document.getElementById("range");

        var range = document.createElement("input");
        range.setAttribute("type", "range");
        range.setAttribute("id", "range");
        range.setAttribute("class", "slider");
        range.setAttribute("name", "range");
        range.setAttribute("min", "1");
        range.setAttribute("max", "10");
        range.setAttribute("value", "5");

        var rangeLabel = document.createElement("range");
        rangeLabel.appendChild(document.createTextNode("Number of Stories"));


        var rangeValueLabel = document.createElement("span");
        rangeValueLabel.setAttribute("class", "slider_label");
        rangeValueLabel.value = range.value;

        range.oninput = function () {
            rangeValueLabel.innerHTML = this.value;
        }

        div.appendChild(rangeLabel);
        div.appendChild(document.createElement("br"));
        div.appendChild(range);
        div.appendChild(rangeValueLabel);
    }

    // Loads the range for the Story Optimization Process
    else if (processType == 'storyOptimization') {

    }
}
