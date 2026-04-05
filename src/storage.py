"""Persistent data access for extracurricular activities."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from models import PersistedData, RegistrationRecord, UserRecord


class ActivityDataStore:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.bootstrap_path = data_path.with_name("bootstrap_data.json")
        self._lock = Lock()

    def list_activities(self) -> dict[str, dict[str, object]]:
        with self._lock:
            data = self._load_data()
            return {
                name: {
                    "description": activity.description,
                    "schedule": activity.schedule,
                    "max_participants": activity.max_participants,
                    "participants": self._participants_for_activity(
                        data, name
                    ),
                }
                for name, activity in data.activities.items()
            }

    def signup(self, activity_name: str, email: str) -> None:
        with self._lock:
            data = self._load_data()
            self._ensure_activity_exists(data, activity_name)

            if email in self._participants_for_activity(data, activity_name):
                raise ValueError("Student is already signed up")

            if email not in data.users:
                data.users[email] = UserRecord(email=email)

            data.registrations.append(
                RegistrationRecord(activity_name=activity_name, user_email=email)
            )
            self._save_data(data)

    def unregister(self, activity_name: str, email: str) -> None:
        with self._lock:
            data = self._load_data()
            self._ensure_activity_exists(data, activity_name)

            for index, registration in enumerate(data.registrations):
                if (
                    registration.activity_name == activity_name
                    and registration.user_email == email
                ):
                    del data.registrations[index]
                    self._save_data(data)
                    return

            raise ValueError("Student is not signed up for this activity")

    def _ensure_activity_exists(
        self, data: PersistedData, activity_name: str
    ) -> None:
        if activity_name not in data.activities:
            raise KeyError(activity_name)

    def _participants_for_activity(
        self, data: PersistedData, activity_name: str
    ) -> list[str]:
        return [
            registration.user_email
            for registration in data.registrations
            if registration.activity_name == activity_name
        ]

    def _load_data(self) -> PersistedData:
        self._bootstrap_runtime_file()
        with self.data_path.open("r", encoding="utf-8") as data_file:
            raw_data = json.load(data_file)
        return PersistedData.model_validate(raw_data)

    def _save_data(self, data: PersistedData) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_path.open("w", encoding="utf-8") as data_file:
            json.dump(data.model_dump(mode="json"), data_file, indent=2)

    def _bootstrap_runtime_file(self) -> None:
        if self.data_path.exists():
            return

        if not self.bootstrap_path.exists():
            raise FileNotFoundError(
                f"Bootstrap data file not found: {self.bootstrap_path}"
            )

        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.bootstrap_path.open("r", encoding="utf-8") as bootstrap_file:
            raw_data = json.load(bootstrap_file)

        data = PersistedData.model_validate(raw_data)
        self._save_data(data)
