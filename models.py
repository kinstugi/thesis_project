from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///db.sqlite3')
Base = declarative_base()
Session = sessionmaker(bind=engine)

question_tags_table = Table(
    'question_tags', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('topic_tag_id', Integer, ForeignKey('topic_tags.id'))
)

class TopicTag(Base):
    __tablename__ = 'topic_tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Define the many-to-many relationship
    questions = relationship("Question", secondary=question_tags_table, back_populates="topic_tags")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    difficulty = Column(String)
    # question_id = Column(Integer, unique=True, nullable=False)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    acceptance = Column(String)
    
    # Define the many-to-many relationship
    topic_tags = relationship("TopicTag", secondary=question_tags_table, back_populates="questions")
    solutions = relationship("Solution", back_populates="question", cascade="all, delete-orphan")


class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="solutions")
    language = Column(String, nullable=False)
    code = Column(String, nullable=False)
    embedding = Column(String)  # Assuming embedding is stored as a string for simplicity, change to pgvector if using PostgreSQL

Base.metadata.create_all(engine)