"""
Base scheme.
"""

from pydantic import BaseModel, field_serializer


class BaseScheme(BaseModel):
    """
    Schema to response.
    """
    id: str | int
    title: str
    description: str

    @field_serializer('id')
    def serialize_id(self, _id: str | int, _info):
        return str(_id)

    class Config:
        from_attributes = True


class BaseSchemeAdd(BaseModel):
    """
    Schema for creation or modification
    """
    title: str
    description: str
