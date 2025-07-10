# insert user with name, email, and password
from datetime import datetime
from bson import ObjectId

from app.db.client import users_table, mongo_to_dict


def insert_user(name, email, password):
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
    users_table.update_one(
        {"_id": ObjectId(user_id)},  # filter
        {"$set": {"token": token}}  # update
    )


def verify_token(token):
    user = users_table.find_one({"token": token})
    if user:
        if user.get("is_blocked", False):
            return None  # User is blocked
        if not user.get("is_active", True):
            return None  # User is not active
        return mongo_to_dict(user)
    return None


# get single user by email and password
def get_user_by_email_and_password(email, password):
    user = users_table.find_one({"email": email, "password": password})
    if user:
        return mongo_to_dict(user)
    return None
