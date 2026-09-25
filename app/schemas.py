from pydantic import BaseModel, Field

class TicketRequest(BaseModel):
    subject: str = Field(min_length=3, max_length=300)
    body: str = Field(min_length=3, max_length=10000)

class BatchRequest(BaseModel):
    items: list[TicketRequest] = Field(min_length=1, max_length=200)

class FeedbackRequest(BaseModel):
    correct_category: str
    notes: str = ""
