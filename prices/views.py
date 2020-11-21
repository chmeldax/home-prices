from django.db import models
from django.db import connection
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from plentific.helpers import dict_fetchall
from prices.models import PropertySale
from prices.serializers import AveragePropertyPriceSerializer, PropertyPriceCountSerializer


class AveragePropertyPriceList(ListAPIView):
    serializer_class = AveragePropertyPriceSerializer

    def get_queryset(self):
        from_date = self.kwargs["from_date"]
        to_date = self.kwargs["to_date"]
        postcode = self.kwargs["postcode"]

        return PropertySale.objects.filter(
            date_of_transfer__range=(from_date, to_date), postcode=postcode
        ).values("property_type", "date_of_transfer").annotate(average_price=models.Avg('price'))


class PropertyPriceCountList(ListAPIView):
    serializer_class = PropertyPriceCountSerializer
    queryset = PropertySale.objects.all()

    def list(self, request, *args, **kwargs):
        from_date = self.kwargs["from_date"]
        to_date = self.kwargs["to_date"]
        postcode = self.kwargs["postcode"]

        # This is done via raw query since it uses fancy Postgres stuff still not supported by Django ORM. Sadly.
        # It generates series (1-8), joins this with CTE meant to retrieve overall minimal and max price.
        # Subsequently, we let Postgres create 8 buckets + we calculate boundaries.
        cursor = connection.cursor()
        cursor.execute("""
            WITH price_stats AS (
                SELECT
                    MIN(price) AS min_price,
                    MAX(price) AS max_price,
                    ROUND((MAX(price) - MIN(price)) / 8::NUMERIC, 2) AS step
                    FROM prices_propertysale
                    WHERE date_of_transfer BETWEEN %(from_date)s AND %(to_date)s AND postcode = %(postcode)s
            )
            SELECT
                (min_price + step * (bucket - 1)) AS bucket_start,
                (min_price + step * (bucket)) AS bucket_end,
                COUNT(*)
            FROM
                generate_series(1, 8) g(bucket)
                CROSS JOIN price_stats ps
                LEFT JOIN prices_propertysale pps
                    ON width_bucket(price, min_price, max_price + 0.01, 8) = g.bucket
            WHERE pps.date_of_transfer BETWEEN %(from_date)s AND %(to_date)s AND pps.postcode = %(postcode)s
            GROUP BY bucket_start, bucket_end
            ORDER BY bucket_start;
        """, {"from_date": from_date, "to_date": to_date, "postcode": postcode})

        result = dict_fetchall(cursor)
        serializer = self.serializer_class(list(result), many=True)
        return Response(serializer.data)
