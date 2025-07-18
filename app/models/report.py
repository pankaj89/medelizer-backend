from pydantic import BaseModel


class TipRequest(BaseModel):
    """Model for tip request data."""
    test_name: str
    summary: str
    parameters: str
