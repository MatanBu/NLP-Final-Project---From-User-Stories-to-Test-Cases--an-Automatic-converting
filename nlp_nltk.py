from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

def Porter_Stemmer(str1):
    """ 
        input: string
        output: string without stop words
    """
    words = word_tokenize(str1)
    out = ""
    
    for word in words:
        out += ps.stem(word) + " "

    return out