from django.core.management.base import BaseCommand
from django.utils import timezone


from prices.models import PropertySale


class Command(BaseCommand):
    """
    This was used to populate DB and generate fixtures.
    This could be deleted, but leaving it so that you know how I achieved that.
    """
    data = {
        "EN36BG": {
            "2020-01-01": {
                "D": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                "S": [11, 21, 31, 41, 51],
                "T": [61, 71, 81, 91],
                "F": [],
            },
            "2020-02-01": {
                "D": [110, 120, 130, 140, 150, 160, 170, 180, 190, 200],
                "S": [111, 121, 131, 141, 151],
                "T": [],
                "F": [161, 171, 181, 191],
            },
        },
        "E106EL": {
            "2020-01-01": {
                "D": [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
                "S": [16, 26, 36, 46, 56],
                "T": [66, 76, 86, 96],
                "F": [],
            },
            "2020-02-01": {
                "D": [115, 125, 135, 145, 155, 165, 175, 185, 195, 205],
                "S": [116, 126, 136, 146, 156],
                "T": [],
                "F": [166, 176, 186, 196],
            },
        }
    }

    def handle(self, *args, **options):
        [
            PropertySale.objects.create(
                postcode=postcode, price=price, date_of_transfer=timezone.datetime.strptime(datetime, "%Y-%m-%d"),
                property_type=property_type
            )
            for postcode, postcode_data in self.data.items()
            for datetime, datetime_data in postcode_data.items()
            for property_type, property_type_data in datetime_data.items()
            for price in property_type_data
        ]
