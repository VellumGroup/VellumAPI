import uuid
from fastapi import APIRouter, Depends, HTTPException
from db.database import supabase
from notes.models import NoteCreate, NoteUpdate, NotePatch, InviteCollaborator
from utils.dependencies import get_current_user, get_user_plan, enforce_limit
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("")
def create_note(note: NoteCreate, user: dict = Depends(get_current_user)):
    plan = get_user_plan(user["id"])
    count_response = supabase.table("notes").select("id", count="exact").eq("owner_id", user["id"]).execute()
    enforce_limit(plan, "notes", count_response.count if count_response.count else 0)
    
    note_id = f"note_{uuid.uuid4().hex}"
    supabase.table("notes").insert({
        "id": note_id,
        "owner_id": user["id"],
        "owner_type": user.get("type", "user"),
        "title": note.title,
        "content": note.content
    }).execute()
    return {"id": note_id, "title": note.title}

@router.get("")
def get_notes(user: dict = Depends(get_current_user)):
    response = supabase.table("notes").select("*").eq("owner_id", user["id"]).execute()
    return {"notes": response.data}

@router.get("/{id}")
def get_note(id: str, user: dict = Depends(get_current_user)):
    response = supabase.table("notes").select("*").eq("id", id).eq("owner_id", user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Note not found")
    return response.data[0]

@router.put("/{id}")
def update_note_full(id: str, note: NoteUpdate, user: dict = Depends(get_current_user)):
    response = supabase.table("notes").update({
        "title": note.title,
        "content": note.content,
        "updated_at": "now()"
    }).eq("id", id).eq("owner_id", user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Note not found")
    return response.data[0]

@router.patch("/{id}")
def update_note_partial(id: str, note: NotePatch, user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in note.dict().items() if v is not None}
    update_data["updated_at"] = "now()"
    response = supabase.table("notes").update(update_data).eq("id", id).eq("owner_id", user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Note not found")
    return response.data[0]

@router.delete("/{id}")
def delete_note(id: str, user: dict = Depends(get_current_user)):
    supabase.table("notes").delete().eq("id", id).eq("owner_id", user["id"]).execute()
    return {"message": "Deleted successfully"}

@router.post("/{id}/invite")
def invite_collaborator(id: str, data: InviteCollaborator, user: dict = Depends(get_current_user)):
    plan = get_user_plan(user["id"])
    count_response = supabase.table("collaborators").select("user_id", count="exact").eq("note_id", id).execute()
    enforce_limit(plan, "collaborators", count_response.count if count_response.count else 0)
    
    supabase.table("collaborators").insert({
        "note_id": id,
        "user_id": data.user_id,
        "role": data.role
    }).execute()
    return {"message": "Collaborator added"}

@router.get("/{id}/collaborators")
def get_collaborators(id: str, user: dict = Depends(get_current_user)):
    response = supabase.table("collaborators").select("*").eq("note_id", id).execute()
    return {"collaborators": response.data}

@router.delete("/{id}/collaborators/{user_id}")
def remove_collaborator(id: str, user_id: str, user: dict = Depends(get_current_user)):
    supabase.table("collaborators").delete().eq("note_id", id).eq("user_id", user_id).execute()
    return {"message": "Collaborator removed"}