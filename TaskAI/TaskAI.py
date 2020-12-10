
import stanza


# list used for paser
list1 = []
#list2 = []
#list3 = []
counted = 0
# list used for sentenceBuilder
list4 = []
result = []
str1 = ""
def parser():
    global str1

    # Uncomment when running for the first time
    #stanza.download('en')
    nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')
    count = 0
    counter = 0
    doc = nlp("Add a background color to cells that can be any RGB color. Be able to change the background color of many cells at once.")
    for i, sentence in enumerate(doc.sentences):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        print(f'====== Sentence {i + 1} tokens ======')
        for word in sentence.words:
            if (word.deprel == "nsubj"):
                 count += 1
                 if (count <= 1):
                    list1.append([word.deprel,word.text,word.id,sentence.words[word.head - 1].text,word.head,word.xpos])
                    list4 = sentenceBuilder(list1[count-1], list2,list3)
            if (word.deprel != "nsubj" and word.deprel != "punct" and word.deprel != "mark"):
                 list1.append([word.deprel, word.text, word.id, sentence.words[word.head - 1].text, word.head, word.xpos])
                 list4 = sentenceBuilder(list1[counter - 1], list2,list3)
        for x in list4:
             str1 = ' '.join(x)
             str1 += "."
             result.append(str1)
    return result


def sentenceBuilder(value, list2,list3):
    global counted
    if(value[0] == "nsubj"):
        list2.append(value[1])
        list3.append(value[1])
    if (value[5] == "VB" or value[5] == "VBG" or value[5] == "VBN" or value[5] == "VBZ" or value[5]=="VBD"):
        counted += 1
    if (counted == 1):
        list2.append(value[1])
    if (counted > 1):
        list3.append(value[1])
    print(list2)
    print(list3)
    return list2,list3
if __name__=='__main__':
    print("result list: " + str(parser()))