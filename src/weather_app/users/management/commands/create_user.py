from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email


class Command(BaseCommand):
    help = "Creates a user in db"

    def handle(self, *args, **options):
        user_model = get_user_model()

        while True:
            email = input("Enter email: ")
            try:
                email = user_model.objects.normalize_email(email)
                validate_email(email)
                break
            except ValidationError:
                print("Invalid email. Please provide a valid email.")

        while True:
            password = getpass("Enter password: ")
            reentered_password = getpass("Re-enter password: ")
            if password == reentered_password:
                break
            else:
                print("Passwords do not match")

        is_superuser = input("Creating superuser (y/n)? ") in "yY"

        # Cannot be service station and superuser,
        # so only check for service station if not superuser
        is_service_station = False
        if not is_superuser:
            is_service_station = input("Creating service station user (y/n)? ") in "yY"

        try:
            # Create user
            user = user_model.objects.create_user(
                email=email,
                password=password,
                is_superuser=is_superuser,
                is_service_station=is_service_station,
            )

            # Show success message
            print(
                "User {} created with id {} and uuid {}".format(
                    user.email, user.pk, user.uuid
                )
            )
        except Exception as e:
            print("User creation failed: {}".format(e))
