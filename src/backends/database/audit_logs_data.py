from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from database.conn import db  

audit_logs_collection = db["audit_logs"]

router = APIRouter(prefix="/audit_logs", tags=["Audit Logs"])

class AuditLog(BaseModel):
    id: Optional[str] = None
    user_id: str = Field(..., description="ID of the user who performed the action")
    action: str = Field(..., description="Description of the action performed")
    metadata: dict = Field(default_factory=dict, description="Additional details about the action")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when the action occurred")

async def log_audit(user_id: str, action: str, metadata: dict = {}):
    log_doc = {
        "user_id": ObjectId(user_id),
        "action": action,
        "metadata": metadata,
        "timestamp": datetime.now(timezone.utc)
    }
    result = await audit_logs_collection.insert_one(log_doc)
    return str(result.inserted_id)

@router.get("/", response_model=List[AuditLog])
async def get_audit_logs():
    logs = await audit_logs_collection.find().to_list(100)
    for log in logs:
        log["id"] = str(log["_id"])
        log["user_id"] = str(log["user_id"])
    return logs
