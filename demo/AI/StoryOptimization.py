#input is a list of text
def StoryOptimization (input):
    suggestions = []
    for i in range(len(input)):
        suggestions[i] = str(input[i]) + " changed."
    return suggestions