import random
from .models import *



def send_otp_code(user_email):
    code = str(random.randint(111111, 999999))
    
    # TODO: Send OTP via email or SMS
    print(f"[Dev] OTP for {user_email} is {code}")
    _, created = OtpData.objects.update_or_create(email = user_email,defaults={'otp':code})
    return created