from pydantic import BaseModel


class TipRequest(BaseModel):
    test_name: str
    summary: str
    parameters: str
