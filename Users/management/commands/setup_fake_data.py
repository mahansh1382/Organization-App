from django.core.management.base import BaseCommand
from django.db import transaction
import random

from Users.models import (
    Comments, Texts, Organization, Address, Users, Authentication, Rols, Provinces, Cites
)

from Users.factories import (
    AuthenticationFactory, RolsFactory, UsersFactory,
    ProvincesFactory, CitesFactory, AddressFactory,
    OrganizationFactory, TextsFactory, CommentsFactory
)

NUM_USERS = 50
NUM_ORGS = 20
NUM_COMMENTS = 200


class Command(BaseCommand):
    help = "Generate fake data for development/testing"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Deleting old data...")
        Comments.objects.all().delete()
        Texts.objects.all().delete()
        Organization.objects.all().delete()
        Address.objects.all().delete()
        Users.objects.all().delete()
        Authentication.objects.all().delete()
        Rols.objects.all().delete()
        Provinces.objects.all().delete()
        Cites.objects.all().delete()

        self.stdout.write("✨ Creating base data...")

        # --- Provinces and Cities (Needed for Address) ---
        self.stdout.write("Creating provinces & cities...")
        provinces = [ProvincesFactory() for _ in range(10)]
        cities = [CitesFactory() for _ in range(20)]

        # --- Addresses (Needs Provinces/Cities) ---
        self.stdout.write("Creating addresses...")
        addresses = [
            AddressFactory(
                provinc_id=random.choice(provinces),
                city_id=random.choice(cities)
            ) for _ in range(40) # Create enough addresses for Users/Orgs
        ]

        # --- Roles (Needed for Users) ---
        self.stdout.write("Creating roles...")
        roles = [RolsFactory() for _ in range(3)]

        # --- Users (Needs Roles, Authentication, Address - which are handled by SubFactory) ---
        self.stdout.write("Creating users...")
        users = [
            UsersFactory(rol_id=random.choice(roles))
            for _ in range(NUM_USERS)
        ]

        # --- Organizations (Needs Users, Address) ---
        self.stdout.write("Creating organizations...")
        orgs = [
            OrganizationFactory(
                owener_id=random.choice(users),
                address_id=random.choice(addresses)
            )
            for _ in range(NUM_ORGS)
        ]

        # --- Texts (Needed for Comments) ---
        self.stdout.write("Creating texts...")
        texts = [TextsFactory() for _ in range(50)]

        # --- Comments (Needs Users, Organizations, Texts) ---
        self.stdout.write("Creating comments...")
        for _ in range(NUM_COMMENTS):
            CommentsFactory(
                user_id=random.choice(users),
                org_id=random.choice(orgs),
                text_id=random.choice(texts),
            )

        self.stdout.write(self.style.SUCCESS("✅ Fake data generated successfully!"))
