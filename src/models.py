"""Domain models for persisted extracurricular data."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ActivityRecord(BaseModel):
    name: str
    description: str
    schedule: str
    max_participants: int


class UserRecord(BaseModel):
    email: str
    role: str = "student"
    created_at: str = Field(default_factory=utc_now)


class MembershipRecord(BaseModel):
    user_email: str
    status: str = "prospect"
    joined_at: str | None = None


class RegistrationRecord(BaseModel):
    activity_name: str
    user_email: str
    created_at: str = Field(default_factory=utc_now)


class PersistedData(BaseModel):
    activities: dict[str, ActivityRecord] = Field(default_factory=dict)
    users: dict[str, UserRecord] = Field(default_factory=dict)
    memberships: dict[str, MembershipRecord] = Field(default_factory=dict)
    registrations: list[RegistrationRecord] = Field(default_factory=list)
