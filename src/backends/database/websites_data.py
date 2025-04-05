from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId

from database.conn import db
from .audit_logs_data import log_audit  

websites_collection = db["websites"]

router = APIRouter(prefix="/websites", tags=["Websites"])

class WebsiteCreate(BaseModel):
    url: str = Field(
        ...,
        pattern="^(https?:\\/\\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\\/\\w .-]*)*\\/?$",
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
        pattern="^(https?:\\/\\/)?([\\da-z.-]+)\\.([a-z.]{2,6})([\\/\\w .-]*)*\\/?$",
        description="Valid website URL."
    )
    owner_id: Optional[str] = Field(None, description="ID of the user who owns the website")

@router.post("/", response_model=WebsiteResponse)
async def create_website(website: WebsiteCreate):
    website_doc = {
        "url": website.url,
        "owner_id": ObjectId(website.owner_id),
        "created_at": datetime.now(timezone.utc)
    }
    result = await websites_collection.insert_one(website_doc)
    website_doc["id"] = str(result.inserted_id)
    website_doc["owner_id"] = str(website_doc["owner_id"])

    # 📘 Log audit for creation
    await log_audit(
        user_id=website.owner_id,
        action="create_website",
        metadata=website_doc
    )

    return website_doc

@router.get("/", response_model=List[WebsiteResponse])
async def get_websites():
    websites = await websites_collection.find().to_list(100)
    for website in websites:
        website["id"] = str(website["_id"])
        website["owner_id"] = str(website["owner_id"])
    return websites

@router.get("/{website_id}", response_model=WebsiteResponse)
async def get_website(website_id: str):
    website = await websites_collection.find_one({"_id": ObjectId(website_id)})
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    website["id"] = str(website["_id"])
    website["owner_id"] = str(website["owner_id"])
    return website

@router.put("/{website_id}", response_model=WebsiteResponse)
async def update_website(website_id: str, website_update: WebsiteUpdate):
    update_data = {k: v for k, v in website_update.dict(exclude_unset=True).items()}
    if "owner_id" in update_data and update_data["owner_id"]:
        update_data["owner_id"] = ObjectId(update_data["owner_id"])
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    updated = await websites_collection.find_one_and_update(
        {"_id": ObjectId(website_id)},
        {"$set": update_data},
        return_document=True  
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Website not found")
    updated["id"] = str(updated["_id"])
    updated["owner_id"] = str(updated["owner_id"])

    # 📘 Log audit for update
    await log_audit(
        user_id=updated["owner_id"],
        action="update_website",
        metadata={"updated_fields": update_data, "website_id": website_id}
    )

    return updated

@router.delete("/{website_id}")
async def delete_website(website_id: str):
    website = await websites_collection.find_one({"_id": ObjectId(website_id)})
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    result = await websites_collection.delete_one({"_id": ObjectId(website_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Website not found")

    # 📘 Log audit for deletion
    await log_audit(
        user_id=str(website["owner_id"]),
        action="delete_website",
        metadata={"deleted_id": website_id, "url": website["url"]}
    )

    return {"message": "Website deleted successfully"}
