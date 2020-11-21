import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from prices.models import PropertySale


class Command(BaseCommand):
    def handle(self, *args, **options):
        # FIXME: This is rather naive implementation.
        # In the real world I would strongly prefer to use COPY command and do it on Postgres server instead.
        file_path = os.path.join(settings.BASE_DIR, "resources", "pp-monthly-update-new-version.csv")

        with open(file_path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            for line in reader:
                date_of_transfer = timezone.make_aware(timezone.datetime.strptime(line[2], "%Y-%m-%d %H:%M"))
                # TODO: This could use get_or_create, but that would require storing identifier in the DB
                PropertySale.objects.create(
                    price=line[1], postcode=line[3], date_of_transfer=date_of_transfer, property_type=line[4]
                )
