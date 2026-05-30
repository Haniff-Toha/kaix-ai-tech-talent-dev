"""
Kaix — Pydantic schemas for API request/response models.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Common
# ──────────────────────────────────────────────
class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    data: dict | list | None = None
    message: str | None = None


class JobResponse(BaseModel):
    """Response for async job submission."""
    job_id: uuid.UUID
    status: str = "pending"
    message: str | None = None


# ──────────────────────────────────────────────
# Onboarding / Profile
# ──────────────────────────────────────────────
class OnboardingRequest(BaseModel):
    """Onboarding form submission — all questions from onboarding_spec.md."""
    name: str | None = None
    current_role: str | None = None
    current_field: str | None = None
    target_role: str
    target_field: str | None = None
    experience_level: str = "beginner"
    years_experience: int = Field(default=0, ge=0, le=50)
    current_skills: list[str] = []
    time_budget_minutes: int = Field(default=60, ge=15, le=300)
    preferred_learning_style: str | None = None
    preferred_study_time: str | None = None
    blockers: list[str] = []
    locale: str = Field(default="id", pattern="^(id|en)$")


class ProfileUpdateRequest(BaseModel):
    """Profile update form submission."""
    name: str | None = None
    current_role: str | None = None
    current_field: str | None = None
    target_role: str | None = None
    target_field: str | None = None
    experience_level: str | None = None
    years_experience: int | None = Field(default=None, ge=0, le=50)
    current_skills: list[str] | None = None
    time_budget_minutes: int | None = Field(default=None, ge=15, le=300)
    preferred_learning_style: str | None = None
    preferred_study_time: str | None = None
    blockers: list[str] | None = None


class ProfileResponse(BaseModel):
    user_id: uuid.UUID
    current_role: str | None
    current_field: str | None
    target_role: str | None
    target_field: str | None
    experience_level: str | None
    years_experience: int | None
    current_skills: list | None
    time_budget_minutes: int
    preferred_learning_style: str | None
    preferred_study_time: str | None
    blockers: list[str] | None
    gap_score: float | None
    onboarding_completed: bool
    updated_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Roadmap
# ──────────────────────────────────────────────
class RoadmapResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    target_role: str | None
    total_phases: int | None
    estimated_months: int | None
    roadmap_json: dict
    is_active: bool
    generated_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Activity Logging
# ──────────────────────────────────────────────
class ActivityLogRequest(BaseModel):
    """Submit a free-text activity log."""
    raw_text: str = Field(..., min_length=3, max_length=2000)
    duration_minutes: int | None = Field(default=None, ge=1, le=720)


class ActivityLogResponse(BaseModel):
    id: uuid.UUID
    raw_text: str
    classified_skill: str | None
    mapped_milestone_id: str | None
    mapped_task_id: str | None
    confidence: float | None
    duration_minutes: int | None
    extracted_topics: list[str] | None
    milestone_progress_delta: float
    needs_confirmation: bool
    confirmed: bool
    logged_at: datetime

    model_config = {"from_attributes": True}


class ActivityConfirmRequest(BaseModel):
    """User confirms which milestone the activity maps to."""
    milestone_id: str


# ──────────────────────────────────────────────
# Streaks
# ──────────────────────────────────────────────
class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: date | None

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Notes
# ──────────────────────────────────────────────
class NoteRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class NoteResponse(BaseModel):
    id: uuid.UUID
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Overview / Dashboard
# ──────────────────────────────────────────────
class OverviewResponse(BaseModel):
    streak: StreakResponse | None
    today_tasks: list[dict]
    milestone_progress: list[dict]
    recent_logs: list[ActivityLogResponse]
    daily_quote: str | None
    active_phase: dict | None


# ──────────────────────────────────────────────
# Chat
# ──────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    locale: str = Field(default="id", pattern="^(id|en)$")


# ──────────────────────────────────────────────
# Courses (Learning Hub)
# ──────────────────────────────────────────────
class CourseRequest(BaseModel):
    """Add a custom learning source."""
    title: str = Field(..., min_length=1, max_length=500)
    platform: str | None = None  # book, udemy, dicoding, youtube, etc.
    url: str | None = None
    linked_milestone_id: str | None = None
    estimated_hours: int | None = Field(default=None, ge=1, le=2000)


class CourseUpdateRequest(BaseModel):
    """Update a course."""
    title: str | None = None
    platform: str | None = None
    url: str | None = None
    linked_milestone_id: str | None = None
    estimated_hours: int | None = None
    completed_hours: float | None = None
    status: str | None = Field(default=None, pattern="^(not_started|in_progress|completed)$")
    is_today_focus: bool | None = None


class CourseResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    platform: str | None
    url: str | None
    linked_milestone_id: str | None
    estimated_hours: int | None
    completed_hours: float
    status: str
    is_today_focus: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CourseSessionRequest(BaseModel):
    """Log a study session for a course."""
    duration_minutes: int = Field(..., ge=1, le=720)
    notes: str | None = Field(default=None, max_length=2000)


class CourseSessionResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    user_id: uuid.UUID
    duration_minutes: int
    notes: str | None
    logged_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Reminders
# ──────────────────────────────────────────────
class ReminderRequest(BaseModel):
    """Create a reminder."""
    type: str = Field(default="daily_task", pattern="^(daily_task|streak_at_risk|weekly_recap|encouragement|course)$")
    channel: str = Field(default="in_app", pattern="^(in_app|email|telegram)$")
    scheduled_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # "20:00"
    days: list[str] = Field(..., min_length=1)  # ["mon","tue",...]
    timezone: str = "Asia/Jakarta"
    label: str | None = None  # custom description
    linked_course_id: uuid.UUID | None = None  # link to a course


class ReminderUpdateRequest(BaseModel):
    """Update a reminder."""
    type: str | None = None
    channel: str | None = None
    scheduled_time: str | None = None
    days: list[str] | None = None
    timezone: str | None = None
    is_active: bool | None = None
    label: str | None = None
    linked_course_id: uuid.UUID | None = None


class ReminderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    type: str
    channel: str
    scheduled_time: str  # serialized as HH:MM
    days: list[str]
    timezone: str
    is_active: bool
    label: str | None = None
    linked_course_id: uuid.UUID | None = None
    last_sent_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# Recommendations
# ──────────────────────────────────────────────
class RecommendationResponse(BaseModel):
    id: uuid.UUID
    source: str
    title: str
    platform_display: str | None
    url: str | None
    instructor: str | None
    level: str | None
    language: str | None
    is_free: bool
    has_certificate: bool | None
    rating: float | None
    skills_covered: list[str] | None
    description_short: str | None

    model_config = {"from_attributes": True}
