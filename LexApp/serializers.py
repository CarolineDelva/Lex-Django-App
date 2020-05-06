from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers


from .models import DimDate, FactReview

class FactSerializer(ModelSerializer):
    class Meta:
        model = FactReview
        fields = "__all__"

class DateSerializer(ModelSerializer):
    class Meta:
        model = DimDate
        fields = "__all__"

# yelp_reviews.serializer
class ByYearSerializer(Serializer):
    # Return the *averages*, not the sum!
    year = serializers.IntegerField()
    stars_average = serializers.FloatField()
    useful_average = serializers.FloatField()
    cool_average = serializers.FloatField()
    funny_average = serializers.FloatField()




