from pydantic import BaseModel, EmailStr, Field


class VerifyEmailSchema(BaseModel):
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")
    
    
class ResendOtpSchema(BaseModel):
    email: EmailStr