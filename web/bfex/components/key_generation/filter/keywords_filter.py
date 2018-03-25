import io
import string
import nltk 
import os

def filter_keywords(keywords):

    #remove any punctuation in the keywords
    #first by replace any punctuation with space, then remove space
    keywords = [''.join(c for c in s if c not in string.punctuation) for s in keywords]
    keywords = [s for s in keywords if s]

    # remove any name in the keywords
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'name.txt')

    name_file = io.open(path, 'r')
    name = name_file.read()
    name = [item.lower() for item in name]

    filtered_keywords = []
    for word in keywords:
       if word not in name:
           filtered_keywords.append(word)
    
    #use nltk pos tag to tag each keyword with tag, use only noun tag

    tag = nltk.pos_tag(filtered_keywords)

    tag_keywords = []

    #result with only keywords with noun tag
    for n in range(len(tag)):
        if tag[n][1] in {"NN","NNS"} :
            tag_keywords.append(tag[n])

    nns_list = []

    for n in range(len(tag_keywords)):
        if tag_keywords[n][1] == "NNS":
            nns_tag = nltk.word_tokenize(tag_keywords[n][0])
            t = nltk.pos_tag(nns_tag)
            if t[0][1] != "NN" :
                nns_list.append(tag_keywords[n][0])

    keywords_list = []
    for n in range(len(tag_keywords)):
        keywords_list.append(tag_keywords[n][0])
    
    keywords_list = [x for x in keywords_list if x not in nns_list]

    return keywords_list