import pytest
from django.test import TestCase, Client
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from yelp_reviews.models import DimDate, FactReview


@pytest.fixture(scope="session")
def client():
    yield APIClient()

@pytest.fixture(scope="function")
def dates_reviews(db):
    date_1 = timezone.now()
    date_2 = date_1 - timezone.timedelta(days=1)

    dim_date_1 = DimDate.objects.create(date=date_1)
    dim_date_2 = DimDate.objects.create(date=date_2)

    fact_review_1 = FactReview.objects.create(
        date=dim_date_1,
        count=2,
        stars=3,
        useful=2,
        funny=5,
        cool=4,
    )

    fact_review_2 = FactReview.objects.create(
        date=dim_date_2,
        count=2,
        stars=5,
        useful=9,
        funny=4,
        cool=3,
    )
    return dim_date_1, dim_date_2, fact_review_1, fact_review_2

