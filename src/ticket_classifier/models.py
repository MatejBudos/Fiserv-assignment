from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low         = "low"
    medium      = "medium"
    high        = "high"
    critical    = "critical"


class Ticket(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class Category(str, Enum):
    TECHNICAL_ISSUE      = "technical issue"
    PRODUCT_INQUIRY      = "product inquiry"
    BILLING_INQUIRY      = "billing inquiry"
    CANCELLATION_REQUEST = "cancellation request"
    ACCOUNT_ACCESS       = "account access"


class Classification(BaseModel):
    category: Category
    priority: Priority
    summary: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
