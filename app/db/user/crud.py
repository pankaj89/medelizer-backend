# insert user with name, email, and password
from datetime import datetime

from bson import ObjectId

from app.db.client import users_table, mongo_to_dict


def insert_user(name, email, password):
    """
    Insert a new user into the database with the provided name, email, and password.
    The token is initialized as an empty string, is_blocked is set to False,
    is_active is set to True, and created_at is set to the current datetime.
    Returns the inserted user's ID.
    """
    user = {
        "name": name,
        "email": email,
        "password": password,
        "token": "",
        "is_blocked": False,
        "is_active": True,
        "created_at": datetime.now()
    }
    users_table.insert_one(user)
    return str(user["_id"])  # Return the inserted user's ID


def update_user(user_id, token):
    """
    Update the user's token in the database based on the provided user_id.
    If the user is found, the token is updated with the new value.
    """
    users_table.update_one(
        {"_id": ObjectId(user_id)},  # filter
        {"$set": {"token": token}}  # update
    )


def verify_token(token):
    """
    Verify the user's token by checking if it exists in the database.
    If the user is found and is not blocked or inactive, return the user's data as a dictionary.
    If the user is blocked or inactive, return None.
    """
    user = users_table.find_one({"token": token})
    if user:
        if user.get("is_blocked", False):
            return None  # User is blocked
        if not user.get("is_active", True):
            return None  # User is not active
        return mongo_to_dict(user)
    return None


def get_user_by_email_and_password(email, password):
    """
    Verify the user's token by checking if it exists in the database.
    If the user is found and is not blocked or inactive, return the user's data as a dictionary.
    If the user is blocked or inactive, return None.
    """
    user = users_table.find_one({"email": email, "password": password})
    if user:
        return mongo_to_dict(user)
    return None
