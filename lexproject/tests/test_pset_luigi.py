import os, sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from unittest import TestCase
import tempfile
import numpy as np

from lexproject.approject.approject.embedding import WordEmbedding


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



    # This test checks if the tokenize function remove unecessary character from string
    def test_tokenize(self):
        # Creating an instance of the WordEmbedding class
        we = WordEmbedding(None, None)
        # Storing a string to a variable
        string = "Hello, I'm Scott"
        # Asserting that the tokenize function returns the right list
        self.assertListEqual(we.tokenize(string), ['hello', "i'm", 'scott'])

    # This test checks if the init function initializes the word list and vector
    def test_init_method_word_embedding(self):
        # Creating a list of words 
        words = ['aa','ba','ca']
        # Creating a numpy array 
        vecs = np.array([[1,2], [3,4], [5,6]])
        # Creating an instance of the WordEmbedding class
        we = WordEmbedding(words, vecs)
        # Assert that initialized words list is equal to word list
        self.assertListEqual(we.words, words)
        # Assert that initialize vector is equal to vectors list 
        np.testing.assert_array_equal(we.vecs, vecs)

    # This test checks that the from_files function returns the WordEmbedding class 
    def test_cls_method_from_file(self):
        # Creating an instance of the from_file with mock test files 
        we = WordEmbedding.from_files('tests/test_words.txt', 'tests/test_vectors.npy')
        # Asserting the above instance is equal to the WordEmbedding class 
        self.assertTrue(isinstance(we, WordEmbedding))

    # This test checks the function returns the sum of the vectors 
    def test_embed_document(self):
        # Creating mock word list 
        words = ['aa','ba','ca']
        # Creating a mock numpy array 
        vecs = np.array([[1,2], [3,4], [5,6]])
        # Creating a WordEmbedding class with the words and vecs
        we = WordEmbedding(words, vecs)
        # Using the embed_document function to take a sum of the vecs 
        test_sum = we.embed_document('aa ba ca d')
        # Asserting that the test_sum is equal to the sum of the mock vectors
        self.assertListEqual(test_sum.tolist(), [9,12])





# Create your tests here.
class TestYelpAPI:

    URL_PREFIX = '/yelp/api/'
   
    def test_dates_list_get(self, client, dates_reviews):
        url = self.URL_PREFIX + 'dates/'
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_dates_retrieve_get(self, client, dates_reviews):
        url = self.URL_PREFIX + 'dates/' + str(dates_reviews[0].id) + '/'
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_facts_review_list_get(self, client, dates_reviews):
        url = self.URL_PREFIX + 'facts/'
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_facts_review_retrieve_get(self, client, dates_reviews):
        url = self.URL_PREFIX + 'facts/' + str(dates_reviews[2].id) + '/'
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_year_review_list_get(self, client, dates_reviews):
        url = self.URL_PREFIX + 'by_year' + "/"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

def test_yelp_endpoint(client, dates_reviews):
    url = '/yelp/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
class TestYelpModels:
    def test_dim_dates_model(self, db):
        date_1 = timezone.now()
        dim_date_1 = DimDate.objects.create(date=date_1)
        date_2 = date_1 - timezone.timedelta(days=2)
        dim_date_1.date = date_2
        dim_date_1.save()
        assert dim_date_1.date == date_2

    def test_fact_review_model(self, db):
        date_1 = timezone.now()
        dim_date_1 = DimDate.objects.create(date=date_1)
        fact_review = FactReview.objects.create(date=dim_date_1)

        fact_review.useful = 20
        fact_review.cool = 10
        fact_review.stars = 7
        fact_review.funny = 6

        fact_review.save()
        assert fact_review.useful == 20
        assert fact_review.cool == 10
        assert fact_review.stars == 7
        assert fact_review.funny == 6



    
