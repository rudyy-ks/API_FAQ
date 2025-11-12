from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from schemas import QuestionCreate, QuestionResponse

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()


@router.post("/", response_model=QuestionResponse, status_code=201)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/{id}", response_model=QuestionResponse)
def get_question(id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{id}", status_code=204)
def delete_question(id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return
