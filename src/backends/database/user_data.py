from flask import Blueprint, request, jsonify, abort
from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Optional
from datetime import datetime, timezone
import bcrypt
from bson import ObjectId
from pymongo import ReturnDocument

from database.conn import db  # Ensure this import points to your connection file

users_collection = db["users"]

users_bp = Blueprint("users", __name__, url_prefix="/users")

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    password: str  # This will be hashed before storing
    role: str = Field(..., pattern="^(admin|user)$")  # Use pattern, not regex

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str] = Field(None, pattern="^(admin|user)$")  # Changed regex to pattern

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = UserCreate(**data)
    except ValidationError as ve:
        return jsonify(ve.errors()), 400

    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        abort(400, description="Email already exists")

    hashed_password = hash_password(user.password)
    user_doc = {
        "name": user.name,
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role,
        "created_at": datetime.now(timezone.utc)
    }
    result = users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id  # Assign the ObjectId

    response_data = {
        "id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc["role"],
        "created_at": user_doc["created_at"]
    }
    return jsonify(response_data), 201

@users_bp.route("/", methods=["GET"])
def get_users():
    users = list(users_collection.find().limit(100))
    response = []
    for u in users:
        response.append({
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"],
            "role": u["role"],
            "created_at": u["created_at"]
        })
    return jsonify(response), 200

@users_bp.route("/<string:user_id>", methods=["GET"])
def get_user(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        abort(400, description="Invalid user ID format")
    if not user:
        abort(404, description="User not found")
    response = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"]
    }
    return jsonify(response), 200

@users_bp.route("/<string:user_id>", methods=["PUT"])
def update_user(user_id: str):
    try:
        data = request.get_json()
        user_update = UserUpdate(**data)
    except ValidationError as ve:
        return jsonify(ve.errors()), 400
    update_data = {k: v for k, v in user_update.dict(exclude_unset=True).items()}
    if not update_data:
        abort(400, description="No update data provided")
    try:
        updated_user = users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
    except Exception:
        abort(400, description="Invalid user ID format")
    if not updated_user:
        abort(404, description="User not found")
    response = {
        "id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"],
        "role": updated_user["role"],
        "created_at": updated_user["created_at"]
    }
    return jsonify(response), 200

@users_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_user(user_id: str):
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        abort(400, description="Invalid user ID format")
    if result.deleted_count == 0:
        abort(404, description="User not found")
    return jsonify({"message": "User deleted successfully"}), 200
