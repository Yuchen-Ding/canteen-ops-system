from pydantic import BaseModel, Field


class AiChatRequest(BaseModel):
    session_id: int | None = None
    message: str = Field(min_length=1, max_length=4000)


class AiChatResponse(BaseModel):
    session_id: int
    answer: str
    messages: list[dict]
