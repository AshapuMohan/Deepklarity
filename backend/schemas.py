from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class EntityBase(BaseModel):
    category: str
    name: str

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizBase(BaseModel):
    url: str
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[QuestionBase]
    related_topics: List[str]

class QuizCreate(BaseModel):
    url: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    related_topics: List[str]
    
    key_entities: Dict[str, List[str]] = Field(default_factory=dict)
    sections: List[str] = Field(default_factory=list)
    quiz: List[QuestionBase] = Field(validation_alias="questions")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator('key_entities', mode='before')
    @classmethod
    def transform_entities(cls, v: Any, info) -> Dict[str, List[str]]:
        # If we get a dictionary, it's already in the right format (e.g. from generated_data)
        if isinstance(v, dict):
            return v
            
        # If it's a list (from SQLAlchemy relationship)
        # Note: 'v' might be the Relationship's InstrumentedList
        if hasattr(v, '__iter__') and not isinstance(v, (str, dict)):
            result = {"people": [], "organizations": [], "locations": []}
            for entity in v:
                # Check if it is an Entity object
                if hasattr(entity, 'category') and hasattr(entity, 'name'):
                    if entity.category in result:
                        result[entity.category].append(entity.name)
                    else:
                        result.setdefault(entity.category, []).append(entity.name)
            return result
        return v

    @field_validator('sections', mode='before')
    @classmethod
    def transform_sections(cls, v: Any) -> List[str]:
        if hasattr(v, '__iter__') and not isinstance(v, str):
            # Check if it's a list of Section objects
            if len(v) > 0 and hasattr(v[0], 'name'):
                return [s.name for s in v]
            # Handle empty list or already list of strings
            return [s.name if hasattr(s, 'name') else s for s in v]
        return v

class QuizList(BaseModel):
    id: int
    url: str
    title: str
    
    class Config:
        from_attributes = True
