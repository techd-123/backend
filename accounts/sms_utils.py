import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_sms_otp(phone_number, otp):
    """
    Send OTP via SMS using 2factor.in API
    Returns True if successful, False otherwise
    """
    try:
        url = f"https://2factor.in/API/V1/{settings.TWO_FACTOR_API_KEY}/SMS/{phone_number}/{otp}/YourAppOTP"
        response = requests.get(url)
        data = response.json()
        
        if data.get("Status") == "Success":
            return True
        logger.error(f"SMS sending failed: {data.get('Details')}")
        return False
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return False