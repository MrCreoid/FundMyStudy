from fastapi import APIRouter, Depends, HTTPException, status
from services.firestore import db
from services.auth_dependency import get_current_user, get_current_user_details
from services.email_service import send_email
from datetime import datetime
import logging

router = APIRouter(prefix="/reminders", tags=["reminders"])
logger = logging.getLogger(__name__)

@router.post("/subscribe")
async def subscribe_reminder(
    data: dict,
    user: dict = Depends(get_current_user_details)
):
    """
    Subscribe for Email alerts for a specific scholarship deadline.
    Uses the email from the authenticated user's token.
    """
    uid = user["uid"]
    email = user.get("email")
    
    scholarship_id = data.get("scholarshipId")
    if not scholarship_id:
        raise HTTPException(status_code=400, detail="Scholarship ID is required")
    
    if not email:
        raise HTTPException(
            status_code=400, 
            detail="Valid email required to subscribe."
        )
    
    # 1. Fetch Scholarship Details (for the Email body)
    sch_doc = db.collection("scholarships").document(scholarship_id).get()
    if not sch_doc.exists:
        raise HTTPException(status_code=404, detail="Scholarship not found")
        
    sch_data = sch_doc.to_dict()
    sch_name = sch_data.get("name", "Scholarship")
    deadline = sch_data.get("deadline", "Unknown Date")
    
    # 2. Save Reminder
    reminder_id = f"{uid}_{scholarship_id}"
    reminder_data = {
        "userId": uid,
        "scholarshipId": scholarship_id,
        "scholarshipName": sch_name,
        "deadline": deadline,
        "email": email,
        "status": "active",
        "createdAt": datetime.utcnow().isoformat(),
        "type": "email"
    }
    
    db.collection("reminders").document(reminder_id).set(reminder_data)
    
    # 3. Send Confirmation Email
    subject = f"🔔 Reminder Set: {sch_name}"
    body = f"Hello,\n\nYou have successfully subscribed to deadline reminders for:\n\n🎓 {sch_name}\n📅 Deadline: {deadline}\n\nWe will notify you 7 days before the deadline.\n\nBest,\nFundMyStudy Team"
    
    email_result = send_email(email, subject, body)
    
    logger.info(f"🔔 Email Reminder set for user {email} on scholarship {scholarship_id}. Status: {email_result['status']}")
    
    return {
        "status": "success",
        "message": "Reminder set successfully",
        "email_status": email_result
    }

@router.get("/")
async def get_my_reminders(uid: str = Depends(get_current_user)):
    """Get list of active reminders for the user"""
    try:
        reminders = []
        docs = db.collection("reminders").where("userId", "==", uid).stream()
        
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            reminders.append(data)
            
        return {"count": len(reminders), "reminders": reminders}
    
    except Exception as e:
        logger.error(f"Error fetching reminders: {e}")
        return {"count": 0, "reminders": []}

@router.post("/test-email")
async def test_email_send(
    data: dict,
    user: dict = Depends(get_current_user_details)
):
    """Debug endpoint to force send an Email to the user"""
    email = user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="User has no email linked")
        
    message = data.get("message", "This is a test email from FundMyStudy.")
    subject = "🛠 FundMyStudy Test Email"
    
    result = send_email(email, subject, message)
    
    return {"result": result, "email": email}
