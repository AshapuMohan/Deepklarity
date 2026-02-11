from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    summary = Column(Text)
    related_topics = Column(JSON)  # Stores list of strings

    questions = relationship("Question", back_populates="quiz")
    entities = relationship("Entity", back_populates="quiz")
    sections = relationship("Section", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question = Column(Text)
    options = Column(JSON)  # Stores list of strings
    answer = Column(String)
    difficulty = Column(String)
    explanation = Column(Text)

    quiz = relationship("Quiz", back_populates="questions")

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    category = Column(String)  # 'people', 'organizations', 'locations'
    name = Column(String)

    quiz = relationship("Quiz", back_populates="entities")

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    name = Column(String)

    quiz = relationship("Quiz", back_populates="sections")
