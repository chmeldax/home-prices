from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from prices.views import AveragePropertyPriceList, PropertyPriceCountList

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'price/averages/from_date/<from_date>/to_date/<to_date>/postcode/<postcode>/',
        AveragePropertyPriceList.as_view()
    ),
    path(
        'price/counts/from_date/<from_date>/to_date/<to_date>/postcode/<postcode>/',
        PropertyPriceCountList.as_view()
    ),
]


urlpatterns = format_suffix_patterns(urlpatterns)
