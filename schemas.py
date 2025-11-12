from pydantic import BaseModel
from datetime import datetime
from typing import List


# Вопросы
class QuestionCreate(BaseModel):
    text: str

    def __init__(self, **data):
        super().__init__(**data)
        if not self.text or not self.text.strip():
            raise ValueError("Text cannot be empty")


class QuestionResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    answers: List['AnswerResponse'] = []

    class Config:
        orm_mode = True


# Ответы
class AnswerCreate(BaseModel):
    user_id: str
    text: str

    def __init__(self, **data):
        super().__init__(**data)
        if not self.text or not self.text.strip():
            raise ValueError("Answer text cannot be empty")
        if not self.user_id or not self.user_id.strip():
            raise ValueError("User ID cannot be empty")


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


QuestionResponse.update_forward_refs()
