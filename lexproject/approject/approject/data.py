
import pandas as pd 
import numpy as np 
import pandas as pd 
import re

def load_glove_words(filename):
    """Load a file containing a list of words as a python list
    use case: 'data/glove.6B.50d.txt'
    :param str filename: path/name to file to load
    :rtype: dict
    """

   
    f = open(filename,'r', encoding='utf8')
    gloveModel = {}
    for line in f:
        splitLines = line.split()
        word = splitLines[0]
        wordEmbedding = np.array([float(value) for value in splitLines[1:]])
        gloveModel[word] = wordEmbedding
    return gloveModel



    
