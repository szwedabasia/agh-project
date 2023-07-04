import re
from fastapi.exceptions import HTTPException


def validate_phone_number(phone_number: str) -> str:
    phone_number_pattern = re.compile("^[0-9]{3}\\-[0-9]{3}\\-[0-9]{3}$")
    if phone_number.isdigit() and len(phone_number) == 9:
        return f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
    if bool(phone_number_pattern.match(phone_number)):
        return phone_number
    else:
        raise HTTPException(
            status_code=400, detail=f"Phone number must be 9 digits long"
        )


def validate_email(email: str) -> str:
    if '@' in email:
        return email
    else:
        raise HTTPException(
            status_code=400, detail=f"Not valid email"
        )