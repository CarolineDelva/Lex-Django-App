from django.contrib import admin

from yelp_reviews.models import DimDate, FactReview

# Register your models here.

class DimDateAdmin(admin.ModelAdmin):
    pass

class FactReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(DimDate, DimDateAdmin)
admin.site.register(FactReview, FactReviewAdmin)

