from django.core.management import call_command
from django.test import TestCase
from mock import Mock, patch
from rest_framework import status

from shiptrader.models import Starship, Listing
from rest_framework.test import APITestCase


class CommandsTestCase(TestCase):
    def setUp(self):
        self.mock_json = {
            "results": [
                {
                    "name": "Death Star",
                    "model": "DS-1 Orbital Battle Station",
                    "manufacturer": "Imperial Department of Military Research, Sienar Fleet Systems",
                    "cost_in_credits": "1000000000000",
                    "length": "120000",
                    "max_atmosphering_speed": "n/a",
                    "crew": "342953",
                    "passengers": "843342",
                    "cargo_capacity": "1000000000000",
                    "consumables": "3 years",
                    "hyperdrive_rating": "4.0",
                    "MGLT": "10",
                    "starship_class": "Deep Space Mobile Battlestation",
                },
                {
                    "name": "Millennium Falcon",
                    "model": "YT-1300 light freighter",
                    "manufacturer": "Corellian Engineering Corporation",
                    "cost_in_credits": "100000",
                    "length": "34.37",
                    "max_atmosphering_speed": "1050",
                    "crew": "4",
                    "passengers": "6",
                    "cargo_capacity": "100000",
                    "consumables": "2 months",
                    "hyperdrive_rating": "0.5",
                    "MGLT": "75",
                    "starship_class": "Light freighter",
                },
                {
                    "name": "X-wing",
                    "model": "T-65 X-wing",
                    "manufacturer": "Incom Corporation",
                    "cost_in_credits": "149999",
                    "length": "12.5",
                    "max_atmosphering_speed": "1050",
                    "crew": "1",
                    "passengers": "0",
                    "cargo_capacity": "110",
                    "consumables": "1 week",
                    "hyperdrive_rating": "1.0",
                    "MGLT": "100",
                    "starship_class": "Starfighter",
                },
            ]
        }

    def tearDown(self):
        Starship.objects.all().delete()

    def test_fetch_starships_command_creates_starships(self):
        with patch(
            "shiptrader.management.commands.fetch_starships.requests"
        ) as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = self.mock_json
            call_command("fetch_starships")
            self.assertEqual(Starship.objects.all().count(), 3)


def starships():
    return [
        {
            "starship_class": "Deep Space Mobile Battlestation",
            "manufacturer": "Imperial Department of Military Research, Sienar Fleet Systems",
            "length": 120_000,
            "hyperdrive_rating": 4.0,
            "cargo_capacity": 1_000_000_000_000,
            "crew": 342_953,
            "passengers": 843_342,
        },
        {
            "starship_class": "Light freighter",
            "manufacturer": "Corellian Engineering Corporation",
            "length": 34.37,
            "hyperdrive_rating": 0.5,
            "cargo_capacity": 100_000,
            "crew": 4,
            "passengers": 6,
        },
        {
            "starship_class": "Starfighter",
            "manufacturer": "Incom Corporation",
            "length": 12.5,
            "hyperdrive_rating": 1.0,
            "cargo_capacity": 110,
            "crew": 1,
            "passengers": 0,
        },
    ]


def listings():
    return [
        {"name": "Listing 1", "ship_type": Starship.objects.all()[0], "price": 200},
        {"name": "Listing 2", "ship_type": Starship.objects.all()[0], "price": 100},
        {"name": "Listing 2", "ship_type": Starship.objects.all()[1], "price": 600},
    ]


class ViewsTestCase(APITestCase):
    def setUp(self):
        for ship in starships():
            Starship.objects.create(**ship)

        for listing in listings():
            Listing.objects.create(**listing)

    def tearDown(self):
        Starship.objects.all().delete()
        Listing.objects.all().delete()

    def test_starship_view_returns_all_starships(self):
        response = self.client.get("/shiptrader/starships/")
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in zip(Starship.objects.all(), response.data["results"]):
            self.assertEqual(item[0].starship_class, item[1]["starship_class"])

    def test_listing_view_returns_all_listings(self):
        response = self.client.get("/shiptrader/listings/")
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in zip(Listing.objects.all(), response.data["results"]):
            self.assertEqual(item[0].name, item[1]["name"])

    def test_listing_view_returns_a_given_ship_type(self):
        starship = Starship.objects.all()[0]
        response = self.client.get(
            f"/shiptrader/listings/?search={starship.starship_class}"
        )
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for listing in response.data["results"]:
            self.assertEqual(listing["ship_type"], starship.id)

    def test_listing_view_returns_in_order_of_price_ascending(self):
        response = self.client.get(f"/shiptrader/listings/?ordering=price")
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual([x["price"] for x in response.data["results"]], [100, 200, 600])

    def test_listing_view_returns_given_ship_type_in_order_of_price_descending(self):
        ship_type = Starship.objects.all()[0].starship_class
        response = self.client.get(
            f"/shiptrader/listings/?search={ship_type}&ordering=-price"
        )
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual([x["price"] for x in response.data["results"]], [200, 100])

    def test_listings_are_ordered_by_created_at_ascending(self):
        response = self.client.get(f"/shiptrader/listings/?ordering=created_at")
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        previous_timestamp = ""
        for listing in response.data["results"]:
            self.assertGreater(listing["created_at"], previous_timestamp)
            previous_timestamp = listing["created_at"]

    def test_listings_are_ordered_by_created_at_descending(self):
        response = self.client.get(f"/shiptrader/listings/?ordering=-created_at")
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        previous_timestamp = "9999"
        for listing in response.data["results"]:
            self.assertLess(listing["created_at"], previous_timestamp)
            previous_timestamp = listing["created_at"]

    def test_a_listing_is_created(self):
        ship = Starship.objects.all()[0]
        data = {"name": "Test1", "price": "999", "ship_type": ship.id}
        response = self.client.post(f"/shiptrader/listings/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_listing = Listing.objects.filter(id=response.data["id"])
        self.assertTrue(new_listing.exists())

    def test_a_listing_can_be_deactivated(self):
        listing = Listing.objects.all()[0]
        listing.active = True
        listing.save
        data = {"active": False}
        response = self.client.patch(f"/shiptrader/listings/{listing.id}", data=data)
        active = Listing.objects.get(id=listing.id).active
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["active"])
        self.assertEqual(response.data["active"], active)

    def test_a_listing_can_be_reactivated(self):
        listing = Listing.objects.all()[0]
        listing.active = False
        listing.save
        data = {"active": True}
        response = self.client.patch(f"/shiptrader/listings/{listing.id}", data=data)
        active = Listing.objects.get(id=listing.id).active
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["active"])
        self.assertEqual(response.data["active"], active)

    def test_listing_other_fields_cannot_be_patched(self):
        listing = Listing.objects.all()[0]
        data = {"price": 1, "name": "Test1"}
        response = self.client.patch(f"/shiptrader/listings/{listing.id}", data=data)
        listing = Listing.objects.get(id=listing.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(listing.name, data["name"])
        self.assertNotEqual(listing.price, data["price"])
