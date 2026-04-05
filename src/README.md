# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Persist activities, users, memberships, and registrations across restarts

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student from an activity                            |

## Data Model

The application now uses persisted domain models with meaningful identifiers:

1. **Activities** - Uses activity name as identifier and stores descriptive metadata.
2. **Users** - Uses email as identifier for student records.
3. **Memberships** - Reserved persisted records for club membership lifecycle.
4. **Registrations** - Links users to activities as separate persisted records.

Bootstrap data lives in src/data/bootstrap_data.json.
Runtime data is written to src/data/runtime_data.json and survives application restarts.
