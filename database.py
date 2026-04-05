from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Course, Lesson, Quiz, QuizScore
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lms.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD: Course ---
def create_course(db: Session, title: str, description: str, instructor_id: int):
    db_course = Course(title=title, description=description, instructor_id=instructor_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_courses(db: Session):
    return db.query(Course).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def delete_course(db: Session, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
        return True
    return False

# --- CRUD: Lesson ---
def create_lesson(db: Session, course_id: int, title: str, content: str):
    db_lesson = Lesson(course_id=course_id, title=title, content=content)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lessons_by_course(db: Session, course_id: int):
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()

def update_lesson_content(db: Session, lesson_id: int, new_content: str):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson:
        lesson.content = new_content
        db.commit()
        db.refresh(lesson)
        return lesson
    return None

# --- CRUD: Quiz ---
def create_quiz(db: Session, lesson_id: int, question_data: str):
    db_quiz = Quiz(lesson_id=lesson_id, question_data=question_data)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def save_quiz_score(db: Session, user_id: int, lesson_id: int, score: int, total: int):
    db_score = QuizScore(user_id=user_id, lesson_id=lesson_id, score=score, total=total)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def get_recent_scores(db: Session, limit=5):
    return db.query(QuizScore).order_by(desc(QuizScore.created_at)).limit(limit).all()
