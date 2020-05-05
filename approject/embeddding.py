import numpy as np 
from .data import load_vectors, load_words, load_data
import re
class WordEmbedding(object):
    def __init__(self, words, vecs):
        # Initializeding with the word list
        self.words = words
        # Initializeding with the vectors
        self.vecs = vecs 

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        
        try:
            # Checking the index of the word list
            idx = self.words.index(word)
            # Return the vector of words in the list
            return self.vecs[idx,:]
            # Raise ValueError if word is outside of list
        except ValueError:
            return None


    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instantiate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        # Applying the class to the text file and verctors file
        return cls(load_words(word_file), load_vectors(vec_file))
    
    
    def tokenize(self, text):
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        # Removing useless chararacters from strings
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        # Applying the tokenize function to the text
        text = self.tokenize(text)
        # Mapping the text 
        vec = map(self.__call__, text)
        # Converting text to word
        return np.sum([i for i in vec if i is not None], axis=0)
  