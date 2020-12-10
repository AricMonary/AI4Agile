import stanza

#input is a list of text
def TaskGeneration (input):
    suggestions = []
    
    suggestions = parser(input)

    return suggestions



str1 = ""
counted = 0
sent = []
#sent.append("Add a background color to cells that can be any RGB color.")
#sent.append("Be able to change the background color of many cells at once.")


def parser(sent):
    try:
        result = []
        str2 = "".join(sent)
        global str1
        # Uncomment when running for the first time
        #stanza.download('en')
        nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse')
        count = 0
        counter = 0
        doc = nlp(str2)
        for i, sentence in enumerate(doc.sentences):
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            for word in sentence.words:
                if (word.deprel == "nsubj"):
                     count += 1
                     if (count <= 1):
                        list1.append([word.deprel,word.text,word.id,sentence.words[word.head - 1].text,word.head,word.xpos])
                        list4 = sentenceBuilder(list1[count-1], list2,list3)
                if (word.deprel != "nsubj" and word.deprel != "punct" and word.deprel != "mark"):
                     list1.append([word.deprel, word.text, word.id, sentence.words[word.head - 1].text, word.head, word.xpos])
                     list4 = sentenceBuilder(list1[counter - 1], list2,list3)
            list4 = [ele for ele in list4 if ele!=[]]
            for x in list4:
                 str1 = ' '.join(x)
                 result.append(str1)
        return result
    except:
        print("Nothing passed into parameters")


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
    return list2,list3


if __name__=='__main__':
    print(parser(sent))