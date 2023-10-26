from keybert import KeyBERT
import nltk
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
import funct_paragrapher
 
nltk.download('stopwords')

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line

kw_model = KeyBERT()
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
r = Rake()


 
def get_keyword_string(doc):
    keywords = []
    for sentence in funct_paragrapher.split_into_sentences(doc):
        r.extract_keywords_from_text(sentence)
        phrases = r.get_ranked_phrases()
        if len(phrases) == 0:
            continue
        keywords.append(phrases[0])
        
    
    
    return keywords
    '''
    keywords = kw_model.extract_keywords(doc)

    lines = ""
    for pair in keywords:
        word = pair[0]
        lines += word + ' '

    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(lines)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    
    if len(nouns) == 0:
        lines = doc
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(lines)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
        if len(nouns) == 0:
            return "noimagefound"

    return nouns
    '''