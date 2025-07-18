from pydantic import BaseModel

class SignupRequest(BaseModel):
    """Model for user signup request data."""
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    """Model for user login request data."""
    email: str
    password: str