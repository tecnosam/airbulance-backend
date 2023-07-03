import os
import time
from pymongo import MongoClient

from dotenv import load_dotenv

from app.security import (
    hash_password,
    verify_password,
    generate_token,
    generate_otp,
    hash_otp,
    verify_otp
)

from bson import ObjectId

load_dotenv()


connection = MongoClient(os.getenv("MONGO_URI"))
db = connection[os.getenv("MONGO_DATABASE")]


def post_request(user_id: str, description: str, location: str):

    collection = db["requests"]

    user_id = ObjectId(user_id)

    request = {
        "user_id": user_id,
        "description": description,
        "location": location,
        "status": "pending",
    }

    result = collection.insert_one(request)

    return {
        'success': result.acknowledged,
        'id': str(result.inserted_id)
    }


def get_request(request_id: str):
    request_id = ObjectId(request_id)
    return db.requests.find_one({"_id": request_id})


def get_requests(status: str = None, user_id: str = None):
    query = {}

    if status:
        query["status"] = status

    if user_id:
        query["user_id"] = ObjectId(user_id)

    result = list(db.requests.find(query))

    return result


def register_user(name, email, password):

    collection = db['users']

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password)
    }

    result = collection.insert_one(user)

    return {
        'success': result.acknowledged,
        'id': str(result.inserted_id)
    }


def login_user(email, password):

    user = db.users.find_one({"email": email})

    if user:

        if verify_password(password, user['password']):
            return {
                "success": True,
                "message": "User logged in",
                "data": {
                    "token": generate_token({
                        "id": str(user['_id'])
                    }),
                    "user": {
                        'name': user['name'],
                        'email': user['email']
                    }
                }
            }

        return {"message": "Incorrect password"}

    return {"message": "User with E-mail not found"}


def update_user(user_id, updates: dict):

    user_id = ObjectId(user_id)

    if "password" in updates:
        updates["password"] = hash_password(updates["password"])

    result = db.users.update_one({"_id": user_id}, {"$set": updates})

    return {
        "success": result.acknowledged,
        "modified_count": result.modified_count
    }


def reset_password(user_id, otp, password):

    user_id = ObjectId(user_id)

    otp_object = db.otp.find_one({"user_id": user_id})

    if otp_object:

        is_verified = verify_otp(otp, otp_object["otp"])
        is_not_expired = otp_object["expires_at"] > time.time()

        if is_verified and is_not_expired:

            db.otp.delete_one({"_id": otp_object["_id"]})

            return update_user(user_id, {"password": password})

        if not is_not_expired:
            # Delete expired OTP
            db.otp.delete_one({"_id": otp_object["_id"]})

        return {
            "success": False,
            "message": "invalid OTP"
        }

    return {
        "success": False,
        "message": "OTP does not belong to this user"
    }


def send_otp(email):

    user = db.users.find_one({"email": email})

    if user:

        user_id = user["_id"]

        otp = generate_otp()
        hashed_otp = hash_otp(otp)

        db.otp.update_one(
            {
                "user_id": user_id
            },
            {
                "$set" {
                    "otp": hashed_otp,
                    "expires_at": time.time() + 300,  # 5 minute
                }
            },
            upsert=True
        )

        return {
            "message": "Sent OTP",
            "otp": otp,  # send raw OTP so frontend can store it
            "user_id": str(user_id)
        }

    return {"message": "User with E-mail not found"}
