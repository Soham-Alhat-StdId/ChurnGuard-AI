from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import schemas
from app.models.database_models import Campaign
from app.services.campaign_service import CampaignService

router = APIRouter()
campaign_service = CampaignService()


@router.post("/", response_model=schemas.Campaign)
def create_campaign(
    campaign: schemas.CampaignCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new campaign
    """
    db_campaign = campaign_service.create_campaign(
        db=db,
        customer_id=campaign.customer_id,
        campaign_type=campaign.campaign_type,
        campaign_name=campaign.campaign_name,
        message_template=campaign.message_template,
        trigger_reason=campaign.trigger_reason,
        trigger_score=campaign.trigger_score
    )
    return db_campaign


@router.post("/{campaign_id}/send")
def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """
    Send a campaign to the customer
    """
    try:
        success = campaign_service.send_campaign(db, campaign_id)
        if success:
            return {"message": "Campaign sent successfully", "campaign_id": campaign_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to send campaign")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/automated/high-risk")
def create_automated_campaigns(
    db: Session = Depends(get_db)
):
    """
    Automatically create campaigns for high-risk customers
    """
    try:
        campaigns = campaign_service.create_automated_campaigns_for_high_risk(db)
        return {
            "message": f"Created {len(campaigns)} automated campaigns",
            "campaigns": campaigns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Campaign])
def list_campaigns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all campaigns with pagination
    """
    campaigns = db.query(Campaign).offset(skip).limit(limit).all()
    return campaigns


@router.get("/{campaign_id}", response_model=schemas.Campaign)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """
    Get campaign by ID
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
