import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, FRONTEND_URL, PLAN_LIMITS
from db.database import supabase
from utils.dependencies import get_current_user
# TODO: MAKE THE DAMN FILE IMPORTS WORK BECAUSE I DONT KNOW HOW

stripe.api_key = STRIPE_SECRET_KEY
router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/plans")
def get_plans():
    return PLAN_LIMITS

@router.post("/checkout")
def create_checkout(user: dict = Depends(get_current_user)):
    if user.get("type") == "guest":
        raise HTTPException(status_code=400, detail="Guests must register to subscribe.")
        
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=user.get("email"),
        line_items=[{"price": "price_pro_tier_id", "quantity": 1}],
        success_url=f"{FRONTEND_URL}/success",
        cancel_url=f"{FRONTEND_URL}/billing",
        metadata={"user_id": user["id"]}
    )
    return {"url": session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]
        user_id = sub["metadata"]["user_id"]
        
        supabase.table("subscriptions").upsert({
            "user_id": user_id,
            "plan": "pro",
            "stripe_customer_id": sub["customer"],
            "stripe_subscription_id": sub["id"],
            "status": sub["status"],
            "current_period_end": sub["current_period_end"]
        }).execute()
        
    return {"status": "success"}