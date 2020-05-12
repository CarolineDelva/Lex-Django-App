import os, sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from unittest import TestCase
import tempfile
import numpy as np

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(0, '../approject/approject/')

#import embedding
from approject.approject.embedding import WordEmbedding



class test_wordembedding(TestCase):

  # This function checks if __call__ function returns none if word is not in the list 
    def test_not_vocabulary(self):
           
        # Creating a fake word list 
        words = ['a','b','c']
        # Creating a mock vector
        vecs = np.array([[1,2], [3,4], [5,6]])
        # Creating an instance of the word embedding class
        we = WordEmbedding(words, vecs)
        # Asserting that 'aaa' which is not in the word list returns none
        self.assertEqual(we('aaa'), None)


    def test_in_vocabulary(self):
           
        # Creating a mock word list 
        words = ['a','b','c']
        # Creating a mock  numpy array
        vecs = np.array([[1,2], [3,4], [5,6]])
        # Creating an instance of the class 
        we = WordEmbedding(words, vecs)
        # Asserting that the list of word is equal to the equivalent list of vectors
        self.assertListEqual(we('a').tolist(), vecs[0,:].tolist())



    # # This test checks if the tokenize function remove unecessary character from string
    # def test_tokenize(self):
    #     # Creating an instance of the WordEmbedding class
    #     we = WordEmbedding(None, None)
    #     # Storing a string to a variable
    #     string = "Hello, I'm Scott"
    #     # Asserting that the tokenize function returns the right list
    #     self.assertListEqual(we.tokenize(string), ['hello', "i'm", 'scott'])

    # # This test checks if the init function initializes the word list and vector
    # def test_init_method_word_embedding(self):
    #     # Creating a list of words 
    #     words = ['aa','ba','ca']
    #     # Creating a numpy array 
    #     vecs = np.array([[1,2], [3,4], [5,6]])
    #     # Creating an instance of the WordEmbedding class
    #     we = WordEmbedding(words, vecs)
    #     # Assert that initialized words list is equal to word list
    #     self.assertListEqual(we.words, words)
    #     # Assert that initialize vector is equal to vectors list 
    #     np.testing.assert_array_equal(we.vecs, vecs)

    # # This test checks that the from_files function returns the WordEmbedding class 
    # def test_cls_method_from_file(self):
    #     # Creating an instance of the from_file with mock test files 
    #     we = WordEmbedding.from_files('tests/test_words.txt', 'tests/test_vectors.npy')
    #     # Asserting the above instance is equal to the WordEmbedding class 
    #     self.assertTrue(isinstance(we, WordEmbedding))

    # # This test checks the function returns the sum of the vectors 
    # def test_embed_document(self):
    #     # Creating mock word list 
    #     words = ['aa','ba','ca']
    #     # Creating a mock numpy array 
    #     vecs = np.array([[1,2], [3,4], [5,6]])
    #     # Creating a WordEmbedding class with the words and vecs
    #     we = WordEmbedding(words, vecs)
    #     # Using the embed_document function to take a sum of the vecs 
    #     test_sum = we.embed_document('aa ba ca d')
    #     # Asserting that the test_sum is equal to the sum of the mock vectors
    #     self.assertListEqual(test_sum.tolist(), [9,12])



