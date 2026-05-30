"""
Kaix — Database models.

Phase 0: users, profiles, roadmaps, activity_logs, streaks, notes,
         user_rag, knowledge_rag, jobs, scraped_courses
Phase 1: courses, course_sessions, reminders
Deferred: focus_sessions, device_tokens
"""

import uuid
from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import settings
from app.db.session import Base


# ──────────────────────────────────────────────
# Users
# ──────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(Text, default="Asia/Jakarta")
    locale: Mapped[str] = mapped_column(Text, default="id")  # "id" or "en"
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    roadmaps: Mapped[list["Roadmap"]] = relationship(back_populates="user")
    activity_logs: Mapped[list["ActivityLog"]] = relationship(back_populates="user")
    streak: Mapped["Streak"] = relationship(back_populates="user", uselist=False)
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    courses: Mapped[list["Course"]] = relationship(back_populates="user")
    reminders: Mapped[list["Reminder"]] = relationship(back_populates="user")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    telegram_connection: Mapped["TelegramConnection"] = relationship(back_populates="user", uselist=False)


# ──────────────────────────────────────────────
# Profiles (one per user, updated in place)
# ──────────────────────────────────────────────
class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    current_role: Mapped[str | None] = mapped_column(Text)
    current_field: Mapped[str | None] = mapped_column(Text)
    target_role: Mapped[str | None] = mapped_column(Text)
    target_field: Mapped[str | None] = mapped_column(Text)
    experience_level: Mapped[str | None] = mapped_column(
        String(20)
    )  # beginner, junior, mid, senior, lead
    years_experience: Mapped[int | None] = mapped_column(Integer)
    current_skills: Mapped[dict | None] = mapped_column(JSONB, default=[])
    time_budget_minutes: Mapped[int] = mapped_column(Integer, default=60)
    preferred_learning_style: Mapped[str | None] = mapped_column(Text)
    preferred_study_time: Mapped[str | None] = mapped_column(Text)
    blockers: Mapped[list | None] = mapped_column(ARRAY(Text))
    gap_score: Mapped[float | None] = mapped_column(Float)
    profile_json: Mapped[dict | None] = mapped_column(JSONB)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="profile")


# ──────────────────────────────────────────────
# Roadmaps (one active per user)
# ──────────────────────────────────────────────
class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_role: Mapped[str | None] = mapped_column(Text)
    total_phases: Mapped[int | None] = mapped_column(Integer)
    estimated_months: Mapped[int | None] = mapped_column(Integer)
    roadmap_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    generated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="roadmaps")


# ──────────────────────────────────────────────
# Activity Logs
# ──────────────────────────────────────────────
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    classified_skill: Mapped[str | None] = mapped_column(Text)
    mapped_milestone_id: Mapped[str | None] = mapped_column(Text)
    mapped_task_id: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Float)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    source_type: Mapped[str | None] = mapped_column(Text)
    extracted_topics: Mapped[list | None] = mapped_column(ARRAY(Text))
    skill_level_signal: Mapped[str | None] = mapped_column(Text)
    milestone_progress_delta: Mapped[float] = mapped_column(Float, default=0)
    needs_confirmation: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    logged_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="activity_logs")


# ──────────────────────────────────────────────
# Streaks
# ──────────────────────────────────────────────
class Streak(Base):
    __tablename__ = "streaks"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[date | None] = mapped_column(Date)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="streak")


# ──────────────────────────────────────────────
# Notes (Overview quick notes)
# ──────────────────────────────────────────────
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notes")


# ──────────────────────────────────────────────
# User RAG (personal vector store per user)
# ──────────────────────────────────────────────
class UserRAGChunk(Base):
    __tablename__ = "user_rag"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(settings.embedding_dimension))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    __table_args__ = (
        Index(
            "ix_user_rag_embedding",
            embedding,
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


# ──────────────────────────────────────────────
# Knowledge RAG (shared career content)
# ──────────────────────────────────────────────
class KnowledgeRAGChunk(Base):
    __tablename__ = "knowledge_rag"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(settings.embedding_dimension))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default={})
    career_track: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    __table_args__ = (
        Index(
            "ix_knowledge_rag_embedding",
            embedding,
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


# ──────────────────────────────────────────────
# Jobs (async task tracking)
# ──────────────────────────────────────────────
class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # pending, running, done, failed
    result: Mapped[dict | None] = mapped_column(JSONB)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )


# ──────────────────────────────────────────────
# Scraped Courses (permanent course store)
# ──────────────────────────────────────────────
class ScrapedCourse(Base):
    __tablename__ = "scraped_courses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    instructor: Mapped[str | None] = mapped_column(Text)
    platform_display: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str | None] = mapped_column(Text)
    level: Mapped[str | None] = mapped_column(Text)
    duration_hours: Mapped[float | None] = mapped_column(Float)
    price_idr_approx: Mapped[int | None] = mapped_column(Integer)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False)
    has_certificate: Mapped[bool | None] = mapped_column(Boolean)
    rating: Mapped[float | None] = mapped_column(Float)
    rating_count: Mapped[int | None] = mapped_column(Integer)
    skills_covered: Mapped[list | None] = mapped_column(ARRAY(Text))
    career_tracks: Mapped[list | None] = mapped_column(ARRAY(Text))
    description_short: Mapped[str | None] = mapped_column(Text)
    topics_covered: Mapped[list | None] = mapped_column(ARRAY(Text))
    is_indonesia_specific: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bahasa_indonesia: Mapped[bool] = mapped_column(Boolean, default=False)
    content_hash: Mapped[str | None] = mapped_column(Text, unique=True)
    last_scraped_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("idx_courses_source", "source"),
        Index("idx_courses_skills", "skills_covered", postgresql_using="gin"),
        Index("idx_courses_tracks", "career_tracks", postgresql_using="gin"),
    )


# ──────────────────────────────────────────────
# Courses (Learning Hub — user-added)
# ──────────────────────────────────────────────
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    platform: Mapped[str | None] = mapped_column(Text)  # book, udemy, dicoding, youtube
    url: Mapped[str | None] = mapped_column(Text)
    linked_milestone_id: Mapped[str | None] = mapped_column(Text)
    estimated_hours: Mapped[int | None] = mapped_column(Integer)
    completed_hours: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(
        String(20), default="in_progress"
    )  # not_started, in_progress, completed
    is_today_focus: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="courses")
    sessions: Mapped[list["CourseSession"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class CourseSession(Base):
    __tablename__ = "course_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    course: Mapped["Course"] = relationship(back_populates="sessions")


# ──────────────────────────────────────────────
# Reminders
# ──────────────────────────────────────────────
class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(Text, default="daily_task")
    channel: Mapped[str] = mapped_column(Text, default="push")  # push, email
    scheduled_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    days: Mapped[list] = mapped_column(ARRAY(Text), nullable=False)
    timezone: Mapped[str] = mapped_column(Text, default="Asia/Jakarta")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    label: Mapped[str | None] = mapped_column(Text)  # custom reminder description
    linked_course_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="SET NULL")
    )
    last_sent_at: Mapped[datetime | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="reminders")


# ──────────────────────────────────────────────
# Notifications (in-app feed)
# ──────────────────────────────────────────────
class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reminder_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reminders.id", ondelete="SET NULL")
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(Text, default="in_app")  # in_app, email, telegram
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notifications")


# ──────────────────────────────────────────────
# Telegram Connection
# ──────────────────────────────────────────────
class TelegramConnection(Base):
    __tablename__ = "telegram_connections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    bot_token: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[str | None] = mapped_column(Text)
    bot_username: Mapped[str | None] = mapped_column(Text)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="telegram_connection")
