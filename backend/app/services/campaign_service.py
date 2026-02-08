from typing import Optional
from sqlalchemy.orm import Session
from app.models.database_models import Campaign, Customer
from app.core.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CampaignService:
    """Service for automated campaign management"""
    
    def __init__(self):
        self.sendgrid_api_key = settings.SENDGRID_API_KEY
        self.twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    
    def create_campaign(
        self,
        db: Session,
        customer_id: int,
        campaign_type: str,
        campaign_name: str,
        message_template: str,
        trigger_reason: str,
        trigger_score: Optional[float] = None
    ) -> Campaign:
        """
        Create a new campaign
        """
        campaign = Campaign(
            customer_id=customer_id,
            campaign_type=campaign_type,
            campaign_name=campaign_name,
            message_template=message_template,
            status="pending",
            trigger_reason=trigger_reason,
            trigger_score=trigger_score
        )
        
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        return campaign
    
    def send_campaign(self, db: Session, campaign_id: int) -> bool:
        """
        Send a campaign (email, SMS, or push)
        """
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        customer = db.query(Customer).filter(Customer.id == campaign.customer_id).first()
        if not customer:
            raise ValueError(f"Customer {campaign.customer_id} not found")
        
        try:
            if campaign.campaign_type == "email":
                success = self._send_email(customer.email, campaign.message_template)
            elif campaign.campaign_type == "sms":
                success = self._send_sms(customer.email, campaign.message_template)  # Assume phone stored in metadata
            elif campaign.campaign_type == "push":
                success = self._send_push(customer.id, campaign.message_template)
            else:
                success = False
            
            if success:
                campaign.status = "sent"
                campaign.sent_at = datetime.utcnow()
            else:
                campaign.status = "failed"
            
            db.commit()
            return success
            
        except Exception as e:
            logger.error(f"Error sending campaign {campaign_id}: {str(e)}")
            campaign.status = "failed"
            db.commit()
            return False
    
    def _send_email(self, email: str, message: str) -> bool:
        """Send email using SendGrid"""
        # Placeholder implementation
        logger.info(f"Sending email to {email}: {message[:50]}...")
        return True
    
    def _send_sms(self, phone: str, message: str) -> bool:
        """Send SMS using Twilio"""
        # Placeholder implementation
        logger.info(f"Sending SMS to {phone}: {message[:50]}...")
        return True
    
    def _send_push(self, customer_id: int, message: str) -> bool:
        """Send push notification"""
        # Placeholder implementation
        logger.info(f"Sending push to customer {customer_id}: {message[:50]}...")
        return True
    
    def create_automated_campaigns_for_high_risk(self, db: Session) -> list:
        """
        Automatically create campaigns for high-risk customers
        """
        high_risk_customers = db.query(Customer).filter(
            Customer.churn_risk_level == 'high'
        ).limit(100).all()
        
        campaigns = []
        for customer in high_risk_customers:
            # Create personalized campaign
            campaign = self.create_campaign(
                db=db,
                customer_id=customer.id,
                campaign_type="email",
                campaign_name=f"Win-back campaign for {customer.name}",
                message_template=self._generate_winback_message(customer),
                trigger_reason="high_churn_risk",
                trigger_score=customer.churn_probability
            )
            campaigns.append(campaign)
        
        return campaigns
    
    def _generate_winback_message(self, customer: Customer) -> str:
        """Generate personalized win-back message"""
        return f"""
        Hi {customer.name},
        
        We've noticed you haven't shopped with us recently and we miss you!
        
        As a valued customer, we'd like to offer you a special 20% discount
        on your next purchase. Use code: WELCOME_BACK
        
        Thank you for being part of our community.
        
        Best regards,
        The Team
        """
