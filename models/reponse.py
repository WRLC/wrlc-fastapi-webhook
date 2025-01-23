"""
Response model
"""
from pydantic import BaseModel, Field


class Response(BaseModel):
    """
    Response object
    """
    status: str = Field(title="Status", examples=["success"])
    data: dict = Field(title="Data", examples=[{"message": "Hello, World!"}])
