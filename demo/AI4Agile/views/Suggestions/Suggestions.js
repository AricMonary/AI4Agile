var suggestionsCreated = false;
var suggestionCount = 0;

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
    var suggestions = document.getElementsByName('suggestion');
    for (i = 0; i < suggestions.length; i++) {
        if (suggestions[i].checked == true) {
            //addSuggestion(suggestions[i]); // INSERT LINE TO CREATE SUGGESTION
        }
    }

    for (i = suggestions.length - 1; i >= 0; i--) {
        if (suggestions[i].checked == true) {
            suggestionDeleted(suggestions[i]);
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
    if (suggestion.childNodes[i].nodeValue == "") {
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

function createIssue() {
    const bodyData = `{
  "update": {},
  "fields": {
    "summary": "Main order flow broken",
    "issuetype": {
      "id": "10000"
    },
    "components": [
      {
        "id": "10000"
      }
    ],
    "project": {
      "id": "10000"
    },
    "description": "YEET"
  }
}`;
    $.ajax
        ({
            type: "POST",
            url: 'https://playingabout.atlassian.net/rest/api/3/issue',
            dataType: 'json',
            headers: {
                'username': "aric.monary@wsu.edu",
                'password': "TBxPhOl7kvPN7oT0Ql8n4BB3",
                'accept': "application/json",
                'contentType': "application/json"
            },
            async: false,
            data: bodyData,
            success: function () {
                alert("Thanks!");
            }
        })
}