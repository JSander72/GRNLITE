from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables from a .env file
load_dotenv()

# Replace with error handling (e.g., try-except block)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    oauth_id = Column(String, unique=True)
    provider = Column(String)
    password = Column(String, nullable=False, default="default_password")
    is_superuser = Column(Boolean, nullable=False, default=False)
    username = Column(String, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    date_joined = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )  # Use timezone-aware datetime


Base.metadata.create_all(engine)


def save_user(oauth_user_data):
    # Check if user already exists
    user = session.query(User).filter_by(oauth_id=oauth_user_data["oauth_id"]).first()
    if not user:
        # Create a new user
        user = User(
            email=oauth_user_data["email"],
            first_name=oauth_user_data["first_name"],
            last_name=oauth_user_data["last_name"],
            oauth_id=oauth_user_data["oauth_id"],
            provider=oauth_user_data["provider"],
            password="default_password",  # Ensure password is set
            is_superuser=False,  # Ensure is_superuser is set
            username=oauth_user_data["email"].split("@")[
                0
            ],  # Generate username from email
            is_staff=False,  # Ensure is_staff is set
            is_active=True,  # Ensure is_active is set
            date_joined=datetime.now(timezone.utc),  # Ensure date_joined is set
        )
        session.add(user)
        print("User created.")
    else:
        # Update existing user
        user.email = oauth_user_data["email"]
        user.first_name = oauth_user_data["first_name"]
        user.last_name = oauth_user_data["last_name"]
        user.provider = oauth_user_data.get("provider")
        print("User updated.")

    # Commit changes to the database
    session.commit()
    return user


# Assume oauth_user_data is obtained from the OAuth provider
oauth_user_data = {
    "email": "example@example.com",
    "first_name": "Example",
    "last_name": "User",
    "oauth_id": "1234567890",
    "provider": "example_provider",
}
user = save_user(oauth_user_data)
print(f"User saved with ID: {user.id}")
