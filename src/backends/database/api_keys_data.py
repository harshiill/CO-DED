from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId

from database.conn import db  
from audit_logs_data import log_audit

api_keys_collection = db["api_keys"]

router = APIRouter(prefix="/api_keys", tags=["API Keys"])

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

@router.post("/", response_model=APIKeyResponse)
async def create_api_key(api_key_data: APIKeyCreate):
    query = {"service_name": api_key_data.service_name}
    if api_key_data.owner_id:
        query["owner_id"] = ObjectId(api_key_data.owner_id)
    existing = await api_keys_collection.find_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="API key for this service already exists for this user.")

    document = {
        "service_name": api_key_data.service_name,
        "api_key": api_key_data.api_key,
        "created_at": datetime.now(timezone.utc)
    }
    if api_key_data.owner_id:
        document["owner_id"] = ObjectId(api_key_data.owner_id)

    result = await api_keys_collection.insert_one(document)
    document["id"] = str(result.inserted_id)
    if "owner_id" in document:
        document["owner_id"] = str(document["owner_id"])

    # Audit log
    await log_audit(
        user_id=document.get("owner_id"),
        action="create_api_key",
        metadata=document
    )

    return document

@router.get("/", response_model=List[APIKeyResponse])
async def get_api_keys():
    keys = await api_keys_collection.find().to_list(100)
    for key in keys:
        key["id"] = str(key["_id"])
        if "owner_id" in key:
            key["owner_id"] = str(key["owner_id"])
    return keys

@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(key_id: str):
    key = await api_keys_collection.find_one({"_id": ObjectId(key_id)})
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
    key["id"] = str(key["_id"])
    if "owner_id" in key:
        key["owner_id"] = str(key["owner_id"])
    return key

@router.put("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(key_id: str, update_data: APIKeyUpdate):
    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items()}
    if "owner_id" in update_dict and update_dict["owner_id"]:
        update_dict["owner_id"] = ObjectId(update_dict["owner_id"])
    if not update_dict:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    updated = await api_keys_collection.find_one_and_update(
        {"_id": ObjectId(key_id)},
        {"$set": update_dict},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="API Key not found")
    updated["id"] = str(updated["_id"])
    if "owner_id" in updated:
        updated["owner_id"] = str(updated["owner_id"])

    # Audit log
    await log_audit(
        user_id=updated.get("owner_id"),
        action="update_api_key",
        metadata={"updated_fields": update_dict}
    )

    return updated

@router.delete("/{key_id}")
async def delete_api_key(key_id: str):
    key = await api_keys_collection.find_one({"_id": ObjectId(key_id)})
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
    result = await api_keys_collection.delete_one({"_id": ObjectId(key_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="API Key not found")

    # Audit log
    await log_audit(
        user_id=str(key.get("owner_id")),
        action="delete_api_key",
        metadata={"deleted_id": key_id}
    )

    return {"message": "API Key deleted successfully"}
