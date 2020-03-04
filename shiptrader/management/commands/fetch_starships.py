from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from shiptrader.models import Starship
import requests


def is_number(string):
    try:
        float(string.replace(",", ""))
    except ValueError:
        return False
    return True


def clean(item):
    if "unknown" in item.lower():
        return
    if "," in item:
        if is_number(item):
            return item.replace(",", "")
    return item


class Command(BaseCommand):

    help = "Retrieve and populate database with Starships from the StarWars API"

    def handle(self, *args, **options):
        try:
            url = f"{settings.SWAPI_BASE_URL}starships/?page=1"
            inserted = 0
            updated = 0
            while True:
                resp = requests.get(url).json()
                for ship in resp["results"]:
                    if isinstance(ship, dict):
                        attrs = {
                            key: clean(ship[key])
                            for key in [field.name for field in Starship._meta.fields]
                            if key in ship
                        }
                        obj, created = Starship.objects.update_or_create(**attrs)
                        if created:
                            inserted += 1
                        else:
                            updated += 1

                if not resp.get("next"):
                    break

                url = resp["next"]

            print(f"{inserted} Starships inserted, {updated} Starships updated!")

        except Exception as e:
            print(e)
            raise CommandError("Something went wrong!")
