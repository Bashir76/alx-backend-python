from django.core.management.base import BaseCommand
from listings.models import Listing


class Command(BaseCommand):
    help = "Seed the database with sample listings data"

    def handle(self, *args, **kwargs):
        sample_listings = [
            {"title": "Cozy Apartment", "description": "A nice place to stay", "price_per_night": 50.00},
            {"title": "Beach House", "description": "Enjoy the sea view", "price_per_night": 150.00},
            {"title": "Mountain Cabin", "description": "Peaceful and quiet retreat", "price_per_night": 100.00},
        ]

        for data in sample_listings:
            Listing.objects.get_or_create(**data)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
