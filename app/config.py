import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
FREE_NOTES = os.getenv("FREE_NOTES")
FREE_COLLAB = os.getenv("FREE_COLLAB")
FREE_VERSIONS = os.getenv("FREE_VERSIONS")
PRO_NOTES = os.getenv("PRO_NOTES")
PRO_COLLAB = os.getenv("PRO_COLLAB")
PRO_VERSIONS = os.getenv("PRO_VERSIONS")

PLAN_LIMITS = {
    "free": {"notes": FREE_NOTES, "collaborators": FREE_COLLAB, "versions": FREE_VERSIONS},
    "pro": {"notes": PRO_NOTES, "collaborators": PRO_COLLAB, "versions": PRO_VERSIONS}
}