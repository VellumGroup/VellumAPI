import uuid
from fastapi import APIRouter, HTTPException
from db.database import supabase
from auth.models import UserRegister, UserLogin, ConvertGuest
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/guest")
def create_guest():
    guest_id = f"guest_{uuid.uuid4().hex}"
    supabase.table("guests").insert({"id": guest_id}).execute()
    return {"token": guest_id, "type": "guest"}

@router.post("/register")
def register(data: UserRegister):
    user_id = f"usr_{uuid.uuid4().hex}"
    try:
        supabase.table("users").insert({
            "id": user_id,
            "email": data.email,
            "password_hash": data.password
        }).execute()
        return {"token": user_id}
    except Exception:
        raise HTTPException(status_code=400, detail="Registration failed")

@router.post("/login")
def login(data: UserLogin):
    response = supabase.table("users").select("id").eq("email", data.email).eq("password_hash", data.password).execute()
    if not response.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": response.data[0]["id"], "token_type": "bearer"}

@router.post("/convert-guest")
def convert_guest(data: ConvertGuest):
    user_id = f"usr_{uuid.uuid4().hex}"
    
    supabase.table("users").insert({
        "id": user_id, 
        "email": data.email, 
        "password_hash": data.password
    }).execute()
    
    supabase.table("notes").update({
        "owner_id": user_id, 
        "owner_type": "user"
    }).eq("owner_id", data.guest_id).eq("owner_type", "guest").execute()
    
    supabase.table("guests").delete().eq("id", data.guest_id).execute()
    
    return {"message": "Migration complete", "token": user_id}