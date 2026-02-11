from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Quiz, Question, Entity, Section
from backend.schemas import QuizCreate, QuizResponse, QuizList
from backend.services import scraper, llm

router = APIRouter(
    prefix="/api/quiz",
    tags=["quiz"]
)

@router.post("/generate", response_model=QuizResponse)
def generate_quiz_endpoint(quiz_request: QuizCreate, db: Session = Depends(get_db)):
    # Check if quiz already exists for this URL
    existing_quiz = db.query(Quiz).filter(Quiz.url == quiz_request.url).first()
    if existing_quiz:
        return existing_quiz

    try:
        # 1. Scrape Wikipedia
        scraped_data = scraper.scrape_wikipedia(quiz_request.url)
        
        # 2. Generate Quiz using LLM
        # We pass the full text to the LLM
        generated_data = llm.generate_quiz(scraped_data["text"], quiz_request.url)
        
        # 3. Save to Database
        # Create Quiz
        db_quiz = Quiz(
            url=quiz_request.url,
            title=generated_data.get("title", scraped_data["title"]),
            summary=generated_data.get("summary", scraped_data["summary"]),
            related_topics=generated_data.get("related_topics", [])
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        
        # Create Questions
        for q_data in generated_data.get("quiz", []):
            db_question = Question(
                quiz_id=db_quiz.id,
                question=q_data["question"],
                options=q_data["options"],
                answer=q_data["answer"],
                difficulty=q_data["difficulty"],
                explanation=q_data["explanation"]
            )
            db.add(db_question)
            
        # Create Entities
        entities = generated_data.get("key_entities", {})
        for category, names in entities.items():
            for name in names:
                db_entity = Entity(
                    quiz_id=db_quiz.id,
                    category=category,
                    name=name
                )
                db.add(db_entity)
                
        # Create Sections
        for section_name in generated_data.get("sections", []):
            db_section = Section(
                quiz_id=db_quiz.id,
                name=section_name
            )
            db.add(db_section)
            
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[QuizList])
def get_quiz_history(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
