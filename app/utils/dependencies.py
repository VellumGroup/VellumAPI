from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db.database import supabase
from config import PLAN_LIMITS
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_response = supabase.table("users").select("*").eq("id", token).execute()
    if user_response.data:
        return user_response.data[0]
    
    guest_response = supabase.table("guests").select("*").eq("id", token).execute()
    if guest_response.data:
        return {"id": guest_response.data[0]["id"], "type": "guest", "plan": "free"}
    
    raise HTTPException(status_code=401, detail="Invalid token")

def get_user_plan(user_id: str) -> str:
    sub_response = supabase.table("subscriptions").select("plan, status").eq("user_id", user_id).execute()
    if sub_response.data and sub_response.data[0]["status"] == "active":
        return sub_response.data[0]["plan"]
    return "free"

def enforce_limit(plan: str, key: str, current: int):
    if current >= PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])[key]:
        raise HTTPException(status_code=403, detail=f"{key} limit reached")