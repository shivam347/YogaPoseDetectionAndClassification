# Yoga Pose Detection - System Running Guide

## Prerequisites

### Required Software
- **Node.js**: v18+ (for frontend)
- **Python**: v3.10+ (for backend)
- **MySQL**: v8.0+ (database)
- **Git**: For version control

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: Minimum 2GB free space
- **Camera**: Working webcam for pose detection
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd yoga-pose-detection
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- Flask 3.0+
- Flask-SQLAlchemy
- Flask-CORS
- PyJWT
- mysql-connector-python
- mediapipe 0.10+
- scikit-learn
- numpy
- pandas
- opencv-python

#### Database Setup

**Create MySQL Database:**
```bash
mysql -u root -p
```

```sql
CREATE DATABASE yoga_pose_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'yoga_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON yoga_pose_db.* TO 'yoga_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Configure Environment Variables:**
Create `.env` file in backend directory:
```bash
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=mysql://yoga_user:your_password@localhost/yoga_pose_db
```

**Run Database Migrations:**
```bash
flask db init      # First time only
flask db migrate -m "Initial migration"
flask db upgrade
```

**Seed Database with Initial Data:**
```bash
python seed_data.py
```

#### Train ML Model (First Time)
```bash
python app/ml/train_model.py
```

This will:
- Load yoga pose dataset
- Train Random Forest classifier
- Save model to `app/ml/model/`
- Display accuracy metrics (target: 90%+)

#### Start Backend Server
```bash
# Development
python run.py

# Or with Flask
flask run --host=0.0.0.0 --port=5000

# Production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Backend will be available at: `http://localhost:5000`

---

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd ../app
```

#### Install Dependencies
```bash
npm install
```

**Key Dependencies:**
- React 18+
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components
- GSAP + ScrollTrigger
- react-webcam
- axios

#### Configure Environment Variables
Create `.env` file in frontend directory:
```bash
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=YogaPose Detection
```

#### Start Development Server
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

#### Build for Production
```bash
npm run build
```

Build output will be in `dist/` directory.

---

## Running the Complete System

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd app
npm run dev
```

**Access Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- API Documentation: http://localhost:5000/api/docs

