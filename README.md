# Yoga Pose Detection App

A full-stack yoga practice application that recommends asanas, guides users through practice sessions, and aims to provide camera-based pose detection feedback.

The project includes a React frontend, a Flask backend API, MySQL persistence, and machine-learning utilities for pose detection using MediaPipe.

## Features

- User registration and login with JWT authentication
- Pain-based yoga asana recommendations
- Asana catalog with images, benefits, instructions, and difficulty levels
- Protected dashboard and profile pages
- Webcam practice screen for pose detection workflow
- Backend APIs for authentication, exercises, practice sessions, and pose detection
- Database migrations and seed data support
- ML utilities for pose landmark extraction and model training

## Tech Stack

### Frontend

- React 19
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui-style component library
- React Router
- Axios
- react-webcam

### Backend

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- PyJWT
- MySQL
- MediaPipe
- OpenCV
- scikit-learn
- pandas and NumPy

## Project Structure

```text
.
+-- app/                         # React frontend
|   +-- public/images/           # Asana images
|   +-- src/
|       +-- components/          # UI, layout, auth, exercise, and pose components
|       +-- context/             # Auth and pose context providers
|       +-- pages/               # App pages
|       +-- services/            # API service modules
|       +-- types/               # TypeScript types
+-- backend/                     # Flask backend
|   +-- app/
|   |   +-- ml/                  # Pose detection and model training code
|   |   +-- models/              # SQLAlchemy models
|   |   +-- routes/              # API route blueprints
|   +-- migrations/              # Alembic migrations
|   +-- requirements.txt
|   +-- run.py                   # Flask entry point
|   +-- seed_data.py             # Initial data seeding
+-- BACKEND_ARCHITECTURE.md
+-- FRONTEND_ARCHITECTURE.md
+-- SYSTEM_RUNNING.md
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- MySQL 8+
- A webcam-enabled browser for practice mode

## Screen-Shots

![categories](<Screenshot 2026-05-28 110824.png>)

![dashboard](<Screenshot 2026-05-28 110906.png>)

![corpse Pose](<Screenshot 2026-05-26 100737.png>)

![Mountain Pose](<Screenshot 2026-05-26 095534.png>)

![Natarajasana Pose](<Screenshot 2026-05-26 094941.png>)

![Cat-Cow Pose](<Screenshot 2026-05-26 095903.png>)


## API Overview

The backend exposes these main API groups:

- `GET /api/health` - Health check
- `POST /api/auth/register` - Register a user
- `POST /api/auth/login` - Log in and receive a token
- `GET /api/exercises` - Fetch exercises/asanas
- `POST /api/pose/detect` - Detect pose from image data
- `/api/practice` - Practice session endpoints

## Development Notes

- The frontend defaults to `http://localhost:5000/api` if `VITE_API_URL` is not set.
- The backend defaults to `mysql://root:password@localhost/yoga_pose_db` if `DATABASE_URL` is not set.
- Camera features require browser camera permission.
- Pose detection depends on the ML model files and MediaPipe landmark extraction.
- For deeper implementation details, see `FRONTEND_ARCHITECTURE.md`, `BACKEND_ARCHITECTURE.md`, and `SYSTEM_RUNNING.md`.

## Known Issue

Pose detection is currently unstable. Before relying on practice feedback, review the implementation in `backend/app/ml/pose_detector.py`, confirm model files exist under `backend/app/ml/model/`, and retrain or debug the model pipeline as needed.
