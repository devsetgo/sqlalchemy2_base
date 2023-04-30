# -*- coding: utf-8 -*-
import secrets
from datetime import datetime, timedelta

start_date = datetime(2015, 8, 20)

data = []
for i in range(10):
    # Generate a random number of days between 0 and 365*8 (8 years)
    days_created = secrets.randbelow(365 * 8)
    days_updated = secrets.randbelow(365 * 8)

    # Add the random number of days to the start date to get the final datetime values
    date_created = start_date + timedelta(days=days_created)
    date_updated = start_date + timedelta(days=days_updated)

    values = {
        "first_name": f"test-{secrets.token_hex(2)}",
        "last_name": f"test-{secrets.token_hex(2)}",
        "email": f"{secrets.token_hex(3)}@Example-{secrets.token_hex(2)}.com",
        "password": None,
        "is_admin": False,
        "date_created": date_created,
        "date_updated": date_updated,
    }

    data.append(values)

print(data)
