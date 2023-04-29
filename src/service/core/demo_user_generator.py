# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta
import uuid
from loguru import logger

start_date = datetime(2015, 8, 20)


def demo_creator(qty: int) -> list:
    """
    Generate a list of demo user data.

    Args:
        qty (int): The number of users to generate.

    Returns:
        list: A list of dictionaries containing user data.
              Each dictionary contains the following keys:
              - first_name: The user's first name.
              - last_name: The user's last name.
              - email: The user's email address.
              - password: The user's password.
              - is_admin: Whether the user is an admin or not.
              - date_created: The date the user was created.
              - date_updated: The date the user was last updated.
    """
    data = []
    while len(data) < qty:
        # Generate random values for each field
        first_name = f"test-{random.randint(0, 99999):03}"
        last_name = f"test-{random.randint(0, 99999):03}"
        email = f"{uuid.uuid4()}@Example-{random.randint(0, 99999):02}.com"
        password = f"{random.randint(0, 99999):04x}"
        is_admin = False
        date_created = start_date + timedelta(days=random.randint(0, 365 * 8))
        date_updated = start_date + timedelta(days=random.randint(0, 365 * 8))

        # Create a dictionary with the generated values
        values = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "is_admin": is_admin,
            "date_created": date_created,
            "date_updated": date_updated,
        }

        # Add the dictionary to the list of data
        data.append(values)

        # Log the new user data
        logger.debug(f"Added new user: {values}")

    # Return the list of data
    return data
