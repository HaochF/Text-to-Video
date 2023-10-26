from flask import Flask, request
from flask import render_template
import requests
import time
import json
import jsonpickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from torch.nn.functional import softmax
from transformers import BertForNextSentencePrediction, BertTokenizer
from gtts import gTTS

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line

model_NSP = BertForNextSentencePrediction.from_pretrained('bert-base-cased')

tokenizer_BERT = BertTokenizer.from_pretrained('bert-base-cased')

model_BERT_BASE = SentenceTransformer('bert-base-nli-mean-tokens')


def BERT_NSP(seq_A, seq_B):
    


    encoded = tokenizer_BERT.encode_plus(seq_A, text_pair=seq_B, return_tensors='pt')

    seq_relationship_logits = model_NSP(**encoded)[0]

    probs = softmax(seq_relationship_logits, dim=1)

    return probs.tolist()[0][0]







def BERT_similarity_desc(desc_A, desc_B):
    descs = [desc_A, desc_B]

    if len(descs[0]) <=1 or len(descs[1]) <= 1:
        return -1

    descembed = model_BERT_BASE.encode(descs)

    score = cosine_similarity(
        [ descembed[1]],
        [ descembed[0]]
    )
    return (score[0][0])

import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

def get_paragraphs(string):
    threshold = 0.25

    sentences = split_into_sentences(re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", string).replace("[", "").replace("]", "").replace("(", "").replace(")", ""))


    output = [sentences[0]]
    paragraph = 0
    for ind in range(1, len(sentences)):
        #print(BERT_NSP(sentences[ind-1], sentences[ind]) * BERT_similarity_desc(sentences[ind-1], sentences[ind]))
    #    if BERT_NSP(sentences[ind-1], sentences[ind])**2 < threshold:
        if BERT_NSP(sentences[ind-1], sentences[ind]) * BERT_similarity_desc(sentences[ind-1], sentences[ind]) < threshold:
            paragraph += 1
            output.append(sentences[ind])
        elif len(output[paragraph]) > 300 or len(split_into_sentences(output[paragraph])) > 1:
            output[paragraph] += "..."
            paragraph += 1
            output.append("..." + sentences[ind]) 
        else:
            output[paragraph] += ' ' + sentences[ind]


    '''
    for section in output:
        print(section)
        print('---------------------------------')
    '''
    return output[:30]



