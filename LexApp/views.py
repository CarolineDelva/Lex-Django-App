from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import ExtractYear

from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import DimDate, FactReview
from .serializers import DateSerializer, FactSerializer, ByYearSerializer


class DateViewSet(ModelViewSet):
    queryset = DimDate.objects.all()
    serializer_class = DateSerializer

class FactViewSet(ModelViewSet):
    queryset = FactReview.objects.all()
    serializer_class = FactSerializer

# yelp_reviews.views
class ByYear(ModelViewSet):

    serializer_class = ByYearSerializer

    def get_queryset(self):
        base = FactReview.objects.all()

        years = DimDate.objects.prefetch_related(
            'fact_reviews').annotate(
                year=ExtractYear(F('date'))).distinct().values_list(
                    'year', flat=True)

        out_queryset = []

        for year in years:
            result = base.filter(date__date__year=year).aggregate(stars_count=Sum('stars'), useful_count=Sum('useful'), cool_count = Sum('cool'), funny_count = Sum('funny'), count_count=Sum('count'))    
            stars_count = result["stars_count"]
            useful_count = result["useful_count"]
            cool_count = result["cool_count"]
            funny_count = result["funny_count"]
            count_count = result["count_count"]

            stars_average = stars_count / count_count
            useful_average = useful_count / count_count
            cool_average = cool_count / count_count
            funny_average = funny_count / count_count

            year_dict = {
                "year": year,
                "stars_average": stars_average,
                "useful_average": useful_average,
                "cool_average": cool_average,
                "funny_average": funny_average
            }
            out_queryset.append(year_dict)


        return out_queryset
        
# yelp_reviews.views
def render_aggregation(request):
    return render(request, "yelp_reviews/index.html", {})
