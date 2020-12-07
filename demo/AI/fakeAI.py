#input is a list of text
def FakeAI1DoingThings (input):
    suggestions = []
    for i in input:
        suggestions[i] = str(i) + " changed."
    return suggestions