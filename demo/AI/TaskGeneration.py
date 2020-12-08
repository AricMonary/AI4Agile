#input is a list of text
def TaskGeneration (input):
    suggestions = []
    for i in range(len(input)):
        suggestions.append(str(input[i]))
    return suggestions