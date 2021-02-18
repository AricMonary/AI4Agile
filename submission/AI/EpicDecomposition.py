from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

#input is a list of text
def EpicDecomposition (input, numberOfClusters):
    #input = epic

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(input)

    true_k = numberOfClusters
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    suggestions = []

    for i in range(true_k):
        suggestions.append('')

    for sentence in input:
        Y = vectorizer.transform([sentence])
        prediction = model.predict(Y)[0]
        suggestions[prediction] = suggestions[prediction] + ' '+ sentence

    for i in range(true_k):
        if suggestions[i] == '':
            suggestions.remove('')

    return suggestions

epic = [
    "The spreadsheet should have Columns A to Z and Rows 1 to 50. The cells should be referenceable from their corresponding name (Example: A1, B42, etc.).", 
    "Cells can reference other cells for expressions or text.", 
    "Cells should be able to evaluate mathematical statements. Arithmetic expressions are represented as trees. Support for addition, subtraction, multiplication, division, and parenthesis.", 
    "Add a background color to cells that can be any RGB color. Be able to change the background color of many cells at once. ", 
    "Allow for color and text changing to be undone. Be able to redo any undone changes. ", 
    "Allow for the contents of the spreadsheet to be saved. Do not preserve the undo/redo system for when the spreadsheet is saved. Select the folder to save the file in.", 
    "Update cells that are referencing other cells when the referenced cell is updated.", 
    "Run as an independent application on Windows.", 
    "Any changes on the spreadsheet should be resolved instantaneously."
]