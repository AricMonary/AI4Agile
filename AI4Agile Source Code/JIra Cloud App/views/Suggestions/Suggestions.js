var paramtersFromURL = {}

var suggestionsCreated = false;
var suggestionCount = 0;
var suggestions = {
    listOfSuggestions: [],
    get list() {
        return this.listOfSuggestions;
    },
    set list(value) {
        this.listOfSuggestions = value;
        renderSuggestions();
    }
}

function getsuggestions() {

    clearSuggestions();
    changeButtonState(false);

    parametersFromURL = getURLParameters();

    processType = parametersFromURL['processType'];
    issueKey = parametersFromURL['parentIssueKey'];

    if (document.getElementById("slider") != null) {
        sliderValue = document.getElementById("slider").value;
        generateSuggestions(processType, issueKey, sliderValue);
    }
    else {
        generateSuggestions(processType, issueKey, 0);
    }
}

function generateSuggestions(processType, issueKey, sliderValue) {
    var jsonOfIssueKey = JSON.stringify({ 'issueKey': issueKey, 'sliderValue': sliderValue });

    insertLoader();

    switch (processType) {
        //for the epic decomposition process
        case 'epicDecomposition':

            //console.log("Epic Decomposition Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "https://ai4agileaibackend.azurewebsites.net/epicDecompositionCreateSuggestions",
                crossDomain: true,
                data: jsonOfIssueKey,
                contentType: "application/json",
                success: function (data) {
                    replyData = JSON.parse(data);
                    suggestions.list = replyData['suggestions'];
                }
            });
            break;

        //for the story optimization process
        case 'storyOptimization':

            //console.log("Story Optimization Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "https://ai4agileaibackend.azurewebsites.net/storyOptimizationCreateSuggestions",
                crossDomain: true,
                data: jsonOfIssueKey,
                contentType: "application/json",
                success: function (data) {
                    replyData = JSON.parse(data);
                    if (replyData['suggestions'].length > 1) {
                        suggestions.list = replyData['suggestions'];
                    }
                    else {
                        suggestions.list = ['No Story Optimization Possible'];
                    }
                }
            });
            break;

        //for the task generation process
        case 'taskGeneration':

            //console.log("Task Generation Generate Suggestions: " + jsonOfIssueKey)

            $.ajax({
                type: "POST",
                url: "https://ai4agileaibackend.azurewebsites.net/taskGenerationCreateSuggestions",
                crossDomain: true,
                data: jsonOfIssueKey,
                contentType: "application/json",
                success: function (data) {
                    replyData = JSON.parse(data);
                    suggestions.list = replyData['suggestions'];
                }
            });
            break;
    }
}

function renderSuggestions() {
    removeLoader();
    var div = document.getElementById('suggestions');
    suggestionsToRender = suggestions.list;
    for (suggestion of suggestionsToRender) {
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
        
        console.log(suggestionsToRender)
        if (suggestion == "No Story Optimization Possible" && suggestionsToRender.length == 1) {
            checkbox.disabled = true;
            label.setAttribute("contenteditable", "false");
        }

        // add the label element to your div
        newDiv.appendChild(checkbox);
        newDiv.appendChild(label);
        newDiv.appendChild(document.createElement("br"));
        div.appendChild(newDiv);
    }

    document.getElementById('selectAll').disabled = false;
    document.getElementById('deselectAll').disabled = false;
}

// For demo button
function createSuggestions() {
    var div = document.getElementById('suggestions');
    suggestionsToRender = suggestions;
    for (suggestion of suggestionsToRender) {
        var newDiv = document.createElement("div");
        newDiv.setAttribute("class", "suggestion")
        // create the necessary elements
        var label = document.createElement("label");
        label.setAttribute("contenteditable", "true");
        label.setAttribute("for", "suggestion");
        label.appendChild(document.createTextNode(suggestion));

        var checkbox = document.createElement("input");
        checkbox.setAttribute('type', 'checkbox');
        checkbox.setAttribute('name', 'suggestion');
        checkbox.setAttribute('class', '')
        //checkbox.setAttribute('checked', 'True');

        // add the label element to your div
        newDiv.appendChild(checkbox);
        newDiv.appendChild(label);
        newDiv.appendChild(document.createElement("br"));
        div.appendChild(newDiv);
    }

    document.getElementById('selectAll').disabled = false;
    document.getElementById('deselectAll').disabled = false;
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

    if (checkedSuggestions.length == 0)
    {
        return;
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
                url: "https://ai4agileaibackend.azurewebsites.net/epicDecompositionCreateIssues",
                crossDomain: true,
                data: JSON.stringify(suggestionsToSend),
                contentType: "application/json",
            });
            break;

        //for the story optimization process
        case 'storyOptimization':

            //console.log("Story Optimization Suggestion Creation: " + JSON.stringify(suggestionsToSend))

            $.ajax({
                type: "POST",
                url: "https://ai4agileaibackend.azurewebsites.net/storyOptimizationCreateIssues",
                crossDomain: true,
                data: JSON.stringify(suggestionsToSend),
                contentType: "application/json",
            });
            break;

        //for the task generation process
        case 'taskGeneration':

            //console.log("Task Generation Suggestion Creation: " + JSON.stringify(suggestionsToSend))

            $.ajax({
                type: "POST",
                url: "https://ai4agileaibackend.azurewebsites.net/taskGenerationCreateIssues",
                crossDomain: true,
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

function populateRange() {
    processType = getURLParameters()['processType'];

    // Loads the range for the Epic Decomposition Process
    if (processType == 'epicDecomposition') {
        var div = document.getElementById("range");

        var range = document.createElement("input");
        range.setAttribute("type", "range");
        range.setAttribute("id", "slider");
        range.setAttribute("class", "slider");
        range.setAttribute("name", "range");
        range.setAttribute("min", "2");
        range.setAttribute("max", "10");
        range.setAttribute("value", "5");

        var rangeLabel = document.createElement("range");
        rangeLabel.appendChild(document.createTextNode("Number of Stories"));

        var rangeValueLabel = document.createElement("span");
        rangeValueLabel.setAttribute("class", "slider_label");
        rangeValueLabel.innerHTML = range.value;

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
        var div = document.getElementById("range");

        var range = document.createElement("input");
        range.setAttribute("type", "range");
        range.setAttribute("id", "slider");
        range.setAttribute("class", "slider");
        range.setAttribute("name", "range");
        range.setAttribute("min", "0");
        range.setAttribute("max", "10");
        range.setAttribute("value", "5");

        var rangeLabel = document.createElement("range");
        rangeLabel.appendChild(document.createTextNode("Degree of Connectivity"));

        var rangeValueLabel = document.createElement("span");
        rangeValueLabel.setAttribute("class", "slider_label");
        rangeValueLabel.innerHTML = range.value;

        range.oninput = function () {
            rangeValueLabel.innerHTML = this.value;
        }

        div.appendChild(rangeLabel);
        div.appendChild(document.createElement("br"));
        div.appendChild(range);
        div.appendChild(rangeValueLabel);
    }
}

function insertLoader() {
    var div = document.getElementById('suggestions');

    var loading = document.createElement("div");
    loading.setAttribute('id', 'loading');
    loading.setAttribute('class', 'loading');

    var loader = document.createElement("div");
    loader.setAttribute('id', 'loader');
    loader.setAttribute('class', 'loader');

    loading.appendChild(loader);

    div.appendChild(loading);
}

function removeLoader() {
    var loading = document.getElementById('loading');
    loading.parentNode.removeChild(loading);
}

function clearSuggestions() {
    var populatedSuggestions = document.getElementsByName('suggestion');
    for (i = populatedSuggestions.length - 1; i >= 0; i--) {
        suggestionDeleted(populatedSuggestions[i]);
    }
}

function changeButtonState(state) {
    document.getElementById('selectAll').disabled = state;
    document.getElementById('deselectAll').disabled = state;
}