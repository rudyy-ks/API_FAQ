from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Answer, Question
from schemas import AnswerCreate, AnswerResponse

router = APIRouter(prefix="/answers", tags=["Answers"])


@router.post("/{question_id}", response_model=AnswerResponse, status_code=201)
def create_answer(
        question_id: int,
        answer: AnswerCreate,
        db: Session = Depends(get_db)
):
    # Проверяем существование вопроса
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db_answer = Answer(
        question_id=question_id,
        user_id=answer.user_id,
        text=answer.text
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.get("/{id}", response_model=AnswerResponse)
def get_answer(id: int, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.delete("/{id}", status_code=204)
def delete_answer(id: int, db: Session = Depends(get_db)):
    answer = db.query(Answer).filter(Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(answer)
    db.commit()
    return
