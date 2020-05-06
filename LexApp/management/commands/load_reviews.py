import os
import csv
from django.utils import timezone

from django.core.management import BaseCommand

from yelp_reviews.models import DimDate, FactReview


APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_FILE = os.path.join(APP_DIR, "yelp_subset_0.csv")

class Command(BaseCommand):
    help = "Load review facts"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--full", action="store_true")

    def handle(self, *args, **options):
        with open(CSV_FILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    date = row["date"]
                    date_obj = timezone.datetime.strptime(date, "%Y-%m-%d")
                except (KeyError, ValueError):
                    continue

                dim_date, _ = DimDate.objects.get_or_create(date=date_obj)

                stars = row.get("stars", 0) or 0
                useful = row.get("useful", 0) or 0
                funny = row.get("funny", 0) or 0
                cool = row.get("cool", 0) or 0
 
                fact_review = FactReview.objects.create(date=dim_date, stars=stars, useful=useful, funny=funny, cool=cool)
                print(f'{dim_date}...{fact_review}')
        for dim_date in DimDate.objects.all():
            fact_reviews_count = dim_date.fact_reviews.count()
            for fact_review in dim_date.fact_reviews.all():
                fact_review.count = fact_reviews_count
                fact_review.save()

