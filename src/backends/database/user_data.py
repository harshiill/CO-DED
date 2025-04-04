from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, timezone
import bcrypt
from bson import ObjectId
from pymongo import ReturnDocument

from database.conn import db  # Ensure this import points to your connection file

users_collection = db["users"]

router = APIRouter(prefix="/users", tags=["Users"])

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

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)
    user_doc = {
        "name": user.name,
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role,
        "created_at": datetime.now(timezone.utc)
    }
    result = await users_collection.insert_one(user_doc)
    user_doc["id"] = str(result.inserted_id)  # Convert ObjectId to string
    return user_doc

@router.get("/", response_model=List[UserResponse])
async def get_users():
    users = await users_collection.find().to_list(100)
    return [{"id": str(u["_id"]), **u} for u in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    update_data = {k: v for k, v in user_update.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    updated_user = await users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user["id"] = str(updated_user["_id"])
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
