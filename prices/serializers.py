from rest_framework import serializers


class AveragePropertyPriceSerializer(serializers.Serializer):
    property_type = serializers.CharField()
    date_of_transfer = serializers.DateTimeField()
    average_price = serializers.IntegerField()


class PropertyPriceCountSerializer(serializers.Serializer):
    bucket_start = serializers.IntegerField()
    bucket_end = serializers.IntegerField()
    count = serializers.IntegerField()
