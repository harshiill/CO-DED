from flask import Blueprint, request, jsonify, abort
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId
from database.conn import db  # Ensure this import points to your connection file

websites_collection = db["websites"]

websites_bp = Blueprint("websites", __name__, url_prefix="/websites")

class WebsiteCreate(BaseModel):
    url: str = Field(
        ...,
        pattern=r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?$",
        description="Valid website URL."
    )
    owner_id: str = Field(..., description="ID of the user who owns the website")

class WebsiteResponse(BaseModel):
    id: str
    url: str
    owner_id: str
    created_at: datetime

class WebsiteUpdate(BaseModel):
    url: Optional[str] = Field(
        None,
        pattern=r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?$",
        description="Valid website URL."
    )
    owner_id: Optional[str] = Field(None, description="ID of the user who owns the website")

def convert_website_doc(doc):
    doc["id"] = str(doc["_id"])
    doc["owner_id"] = str(doc["owner_id"])
    doc.pop("_id", None)
    return doc

@websites_bp.route("/", methods=["POST"])
def create_website():
    try:
        data = request.get_json()
        website = WebsiteCreate(**data)
    except ValidationError as ve:
        return jsonify(ve.errors()), 400

    website_doc = {
        "url": website.url,
        "owner_id": ObjectId(website.owner_id),
        "created_at": datetime.now(timezone.utc)
    }
    result = websites_collection.insert_one(website_doc)
    website_doc["_id"] = result.inserted_id
    website_doc["owner_id"] = str(website_doc["owner_id"])
    response_data = {
        "id": str(website_doc["_id"]),
        "url": website_doc["url"],
        "owner_id": website_doc["owner_id"],
        "created_at": website_doc["created_at"]
    }
    return jsonify(response_data), 201

@websites_bp.route("/", methods=["GET"])
def get_websites():
    websites = list(websites_collection.find().limit(100))
    response = []
    for website in websites:
        website_data = {
            "id": str(website["_id"]),
            "url": website["url"],
            "owner_id": str(website["owner_id"]),
            "created_at": website["created_at"]
        }
        response.append(website_data)
    return jsonify(response), 200

@websites_bp.route("/<string:website_id>", methods=["GET"])
def get_website(website_id: str):
    try:
        website = websites_collection.find_one({"_id": ObjectId(website_id)})
    except Exception:
        abort(400, description="Invalid website ID format")
    if not website:
        abort(404, description="Website not found")
    response_data = {
        "id": str(website["_id"]),
        "url": website["url"],
        "owner_id": str(website["owner_id"]),
        "created_at": website["created_at"]
    }
    return jsonify(response_data), 200

@websites_bp.route("/<string:website_id>", methods=["PUT"])
def update_website(website_id: str):
    try:
        data = request.get_json()
        website_update = WebsiteUpdate(**data)
    except ValidationError as ve:
        return jsonify(ve.errors()), 400

    update_data = {k: v for k, v in website_update.dict(exclude_unset=True).items()}
    if "owner_id" in update_data and update_data["owner_id"]:
        try:
            update_data["owner_id"] = ObjectId(update_data["owner_id"])
        except Exception:
            abort(400, description="Invalid owner_id format")
    if not update_data:
        abort(400, description="No update data provided")
    
    try:
        updated = websites_collection.find_one_and_update(
            {"_id": ObjectId(website_id)},
            {"$set": update_data},
            return_document=True  # Return the updated document
        )
    except Exception:
        abort(400, description="Invalid website ID format")
    if not updated:
        abort(404, description="Website not found")
    response_data = {
        "id": str(updated["_id"]),
        "url": updated["url"],
        "owner_id": str(updated["owner_id"]),
        "created_at": updated["created_at"]
    }
    return jsonify(response_data), 200

@websites_bp.route("/<string:website_id>", methods=["DELETE"])
def delete_website(website_id: str):
    try:
        result = websites_collection.delete_one({"_id": ObjectId(website_id)})
    except Exception:
        abort(400, description="Invalid website ID format")
    if result.deleted_count == 0:
        abort(404, description="Website not found")
    return jsonify({"message": "Website deleted successfully"}), 200
