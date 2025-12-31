"""Database models for CEO Personal OS Bot"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    timezone = Column(String(50), default='UTC')
    daily_reminder_time = Column(String(10), default='18:00')  # HH:MM format
    weekly_reminder_day = Column(String(10), default='Friday')  # Day of week
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Context fields
    name = Column(String(255))
    role = Column(String(255))
    company = Column(String(255))
    stage_of_life = Column(Text)

    # Relationships
    daily_checkins = relationship('DailyCheckin', back_populates='user', cascade='all, delete-orphan')
    weekly_reviews = relationship('WeeklyReview', back_populates='user', cascade='all, delete-orphan')
    quarterly_reviews = relationship('QuarterlyReview', back_populates='user', cascade='all, delete-orphan')
    annual_reviews = relationship('AnnualReview', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('Goal', back_populates='user', cascade='all, delete-orphan')
    patterns = relationship('Pattern', back_populates='user', cascade='all, delete-orphan')
    interviews = relationship('Interview', back_populates='user', cascade='all, delete-orphan')

class DailyCheckin(Base):
    __tablename__ = 'daily_checkins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    energy_level = Column(Integer)  # 1-10
    meaningful_win = Column(Text)
    friction_point = Column(Text)
    let_go = Column(Text)
    priority_tomorrow = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='daily_checkins')

class WeeklyReview(Base):
    __tablename__ = 'weekly_reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week_start = Column(DateTime, nullable=False)
    moved_needle = Column(Text)
    noise = Column(Text)
    time_leak = Column(Text)
    avg_energy = Column(Integer)
    energy_sources = Column(Text)
    energy_drains = Column(Text)
    strategic_insight = Column(Text)
    adjustment = Column(Text)
    wins = Column(Text)
    open_loops = Column(Text)
    top_priorities = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='weekly_reviews')

class QuarterlyReview(Base):
    __tablename__ = 'quarterly_reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quarter = Column(String(10), nullable=False)  # e.g., "2025-Q1"
    year = Column(Integer, nullable=False)
    goal_progress = Column(Text)
    outcomes = Column(Text)
    time_energy_analysis = Column(Text)
    misalignment = Column(Text)
    energy_avg = Column(Integer)
    output_rating = Column(Integer)
    life_map_ratings = Column(Text)  # JSON string
    stop_doing = Column(Text)
    start_doing = Column(Text)
    continue_doing = Column(Text)
    summary = Column(Text)
    key_insight = Column(Text)
    focus_next_quarter = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='quarterly_reviews')

class AnnualReview(Base):
    __tablename__ = 'annual_reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    year = Column(Integer, nullable=False)
    executive_summary = Column(Text)
    what_went_well = Column(Text)
    peak_experiences = Column(Text)
    what_went_poorly = Column(Text)
    trough_experiences = Column(Text)
    positive_patterns = Column(Text)
    negative_patterns = Column(Text)
    life_dimensions = Column(Text)  # JSON string
    repeat_10_times = Column(Text)
    goal_review = Column(Text)
    letting_go = Column(Text)
    gratitude = Column(Text)
    stop_start_continue = Column(Text)
    word_of_year = Column(String(100))
    summary = Column(Text)
    intent_next_year = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='annual_reviews')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_type = Column(String(20), nullable=False)  # '1_year', '3_year', '10_year'
    category = Column(String(50))  # Career, Relationships, Health, etc.
    title = Column(String(500), nullable=False)
    description = Column(Text)
    why_matters = Column(Text)
    measurement = Column(Text)
    milestones = Column(Text)  # JSON string
    blockers = Column(Text)
    status = Column(String(20), default='active')  # active, achieved, abandoned
    progress_rating = Column(Integer)  # 1-10
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='goals')

class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pattern_type = Column(String(20), nullable=False)  # 'positive', 'negative', 'theme'
    name = Column(String(500), nullable=False)
    description = Column(Text)
    first_observed = Column(String(100))
    evidence = Column(Text)
    why_happens = Column(Text)
    cost = Column(Text)
    how_to_change = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='patterns')

class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    interview_type = Column(String(50), nullable=False)  # 'identity', 'past_year', 'future_self'
    responses = Column(Text)  # JSON string with all Q&A
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='interviews')

# Database initialization
def init_db(database_url='sqlite:///ceo_personal_os.db'):
    """Initialize the database"""
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_session(database_url='sqlite:///ceo_personal_os.db'):
    """Get a database session"""
    engine = create_engine(database_url, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()
