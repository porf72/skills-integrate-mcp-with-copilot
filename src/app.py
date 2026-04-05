"""High School Management System API.

A FastAPI application that allows students to view and sign up for
extracurricular activities at Mergington High School.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from storage import ActivityDataStore

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

activity_store = ActivityDataStore(current_dir / "data" / "runtime_data.json")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activity_store.list_activities()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    try:
        activity_store.signup(activity_name, email)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Activity not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    try:
        activity_store.unregister(activity_name, email)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Activity not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"message": f"Unregistered {email} from {activity_name}"}
