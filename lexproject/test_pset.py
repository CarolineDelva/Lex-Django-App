from django.test import TestCase, Client
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


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



    
