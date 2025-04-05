from flask import Blueprint, request, jsonify, abort
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId
from database.conn import db  # assuming this is a synchronous connection

api_keys_collection = db["api_keys"]

api_keys_bp = Blueprint("api_keys", __name__, url_prefix="/api_keys")

# Pydantic models for validation and documentation
class APIKeyCreate(BaseModel):
    service_name: str = Field(..., description="Name of the API service.")
    api_key: str = Field(..., min_length=32, description="API key hash must be at least 32 characters long.")
    owner_id: Optional[str] = Field(None, description="ID of the user who owns the API key.")

class APIKeyResponse(BaseModel):
    id: str
    service_name: str
    api_key: str
    owner_id: Optional[str] = None
    created_at: datetime

class APIKeyUpdate(BaseModel):
    service_name: Optional[str] = None
    api_key: Optional[str] = Field(None, min_length=32, description="API key hash must be at least 32 characters long.")
    owner_id: Optional[str] = None

# Helper function to convert Mongo document to dict with proper types
def convert_api_key_doc(doc):
    doc["id"] = str(doc["_id"])
    if "owner_id" in doc and doc.get("owner_id") is not None:
        doc["owner_id"] = str(doc["owner_id"])
    # Remove Mongo's internal _id field from response if desired
    doc.pop("_id", None)
    return doc

@api_keys_bp.route("/", methods=["POST"])
def create_api_key():
    try:
        # Validate input using Pydantic
        data = APIKeyCreate(**request.get_json())
    except ValidationError as ve:
        return jsonify(ve.errors()), 400

    query = {"service_name": data.service_name}
    if data.owner_id:
        query["owner_id"] = ObjectId(data.owner_id)
    existing = api_keys_collection.find_one(query)
    if existing:
        abort(400, description="API key for this service already exists for this user.")

    document = {
        "service_name": data.service_name,
        "api_key": data.api_key,
        "created_at": datetime.now(timezone.utc)
    }
    if data.owner_id:
        document["owner_id"] = ObjectId(data.owner_id)

    result = api_keys_collection.insert_one(document)
    document["_id"] = result.inserted_id
    response_data = convert_api_key_doc(document)
    return jsonify(response_data), 201

@api_keys_bp.route("/", methods=["GET"])
def get_api_keys():
    keys = list(api_keys_collection.find().limit(100))
    response = [convert_api_key_doc(key) for key in keys]
    return jsonify(response), 200

@api_keys_bp.route("/<string:key_id>", methods=["GET"])
def get_api_key(key_id: str):
    try:
        key = api_keys_collection.find_one({"_id": ObjectId(key_id)})
    except Exception:
        abort(400, description="Invalid key ID format")
    if not key:
        abort(404, description="API Key not found")
    response = convert_api_key_doc(key)
    return jsonify(response), 200

@api_keys_bp.route("/<string:key_id>", methods=["PUT"])
def update_api_key(key_id: str):
    try:
        update_data = APIKeyUpdate(**request.get_json())
    except ValidationError as ve:
        return jsonify(ve.errors()), 400

    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items()}
    if "owner_id" in update_dict and update_dict["owner_id"]:
        try:
            update_dict["owner_id"] = ObjectId(update_dict["owner_id"])
        except Exception:
            abort(400, description="Invalid owner_id format")
    if not update_dict:
        abort(400, description="No update data provided")
    
    result = api_keys_collection.find_one_and_update(
        {"_id": ObjectId(key_id)},
        {"$set": update_dict},
        return_document=True  # Return the updated document
    )
    if not result:
        abort(404, description="API Key not found")
    response = convert_api_key_doc(result)
    return jsonify(response), 200

@api_keys_bp.route("/<string:key_id>", methods=["DELETE"])
def delete_api_key(key_id: str):
    try:
        result = api_keys_collection.delete_one({"_id": ObjectId(key_id)})
    except Exception:
        abort(400, description="Invalid key ID format")
    if result.deleted_count == 0:
        abort(404, description="API Key not found")
    return jsonify({"message": "API Key deleted successfully"}), 200
