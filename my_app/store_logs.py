import os
import json
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_app.settings")
django.setup()

User = get_user_model()


# Function to process and store log data
def process_and_store_log(log_entry):
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO auth0_logs (date, type, description, client_id, user_id, ip_address, user_agent, details)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            data = (
                log_entry["date"],
                log_entry["type"],
                log_entry["description"],
                log_entry["client_id"],
                log_entry.get("user_id"),  # Handle potential missing user_id
                log_entry["ip"],
                log_entry["user_agent"],
                json.dumps(log_entry["details"]),
            )

            cursor.execute(sql, data)

    except Exception as error:
        print("Error while connecting to PostgreSQL:", error)


# Main function to fetch log data and store it
def main():
    # Assuming log_data is fetched from somewhere within your Django app
    log_data = [
        # Example log data
        {
            "date": "2023-10-01T12:00:00Z",
            "type": "login",
            "description": "User logged in",
            "client_id": "example_client_id",
            "user_id": 1,  # Example user ID
            "ip": "192.168.1.1",
            "user_agent": "Mozilla/5.0",
            "details": {"example_detail": "detail_value"},
        },
        # Add more log entries as needed
    ]

    if log_data:
        for log_entry in log_data:
            process_and_store_log(log_entry)
    else:
        print("No log data found.")


if __name__ == "__main__":
    main()
