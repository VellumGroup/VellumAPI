from fastapi import APIRouter, Depends
from db.database import supabase
from utils.dependencies import get_current_user
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {"id": user.get("id"), "email": user.get("email"), "type": user.get("type", "user")}

@router.get("/me/usage")
def get_usage(user: dict = Depends(get_current_user)):
    count_response = supabase.table("notes").select("id", count="exact").eq("owner_id", user["id"]).execute()
    current_notes = count_response.count if count_response.count else 0
    
    return {
        "user_id": user["id"],
        "plan": user.get("plan", "free"),
        "notes_used": current_notes
    }