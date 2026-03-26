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

### Production Mode

**Using Docker Compose:**
```bash
docker-compose up -d
```

**Manual Production Setup:**
```bash
# Backend
cd backend
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Frontend (serve with nginx or similar)
cd app
npm run build
# Copy dist/ to web server directory
```

---

## Application Workflow

### 1. User Registration/Login
1. Navigate to http://localhost:5173
2. Click "Register" to create account
3. Or click "Login" for existing users
4. JWT token stored for authenticated requests

### 2. Select Pain Type
1. After login, user sees pain selection page
2. Options: Neck Pain, Back Pain, Shoulder Pain, Knee Pain, Stress Relief, General
3. Click on pain type to see recommended asanas

### 3. Browse Asanas
1. Grid of asanas for selected pain type
2. Each card shows:
   - Asana image
   - English and Sanskrit name
   - Brief benefits
   - Difficulty level
3. Click card to view details

### 4. Asana Detail Page
1. Large asana image
2. Detailed benefits list
3. Step-by-step instructions
4. "Start Practice" button with camera icon

### 5. Practice Mode
1. Click camera icon to start
2. Browser requests camera permission
3. Camera feed appears with pose overlay
4. MediaPipe detects body landmarks
5. Random Forest classifier identifies pose
6. Real-time accuracy percentage displayed
7. Feedback on form corrections

### 6. Save Progress
1. Practice session automatically saved
2. View history in profile/dashboard
3. Track improvement over time

---

## ML Model Details

### Pose Detection Pipeline
1. **Video Capture**: Webcam stream from browser
2. **Frame Processing**: MediaPipe Pose extracts 33 landmarks
3. **Feature Extraction**: 132 features (x, y, z, visibility per landmark)
4. **Classification**: Random Forest predicts pose class
5. **Accuracy Calculation**: Compare with reference pose angles
6. **Feedback Generation**: Suggest corrections based on deviations

### Supported Poses (20+ Poses)

**Neck Pain Relief:**
- Neck Stretch (Greeva Sanchalana)
- Neck Roll
- Chin Tuck
- Upper Trapezius Stretch

**Back Pain Relief:**
- Cat-Cow Pose (Bitilasana Marjaryasana)
- Child's Pose (Balasana)
- Cobra Pose (Bhujangasana)
- Bridge Pose (Setu Bandhasana)

**Shoulder Pain Relief:**
- Shoulder Roll
- Eagle Arms (Garudasana Arms)
- Thread the Needle
- Puppy Pose (Uttana Shishosana)

**Knee Pain Relief:**
- Chair Pose (Utkatasana)
- Warrior I (Virabhadrasana I)
- Warrior II (Virabhadrasana II)
- Supported Squat

**Stress Relief:**
- Corpse Pose (Savasana)
- Legs Up Wall (Viparita Karani)
- Easy Pose (Sukhasana)
- Forward Fold (Uttanasana)

**General Poses:**
- Mountain Pose (Tadasana)
- Tree Pose (Vrksasana)
- Downward Dog (Adho Mukha Svanasana)
- Plank Pose (Phalakasana)

### Model Performance
- **Algorithm**: Random Forest Classifier
- **Features**: 132 (33 landmarks × 4 values)
- **Target Accuracy**: 90%+
- **Inference Time**: <50ms per frame
- **Training Data**: 5000+ labeled pose samples

---

## API Testing

### Using curl

**Register User:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Get Exercises:**
```bash
curl http://localhost:5000/api/exercises?pain_type=neck
```

**Detect Pose (with image):**
```bash
curl -X POST http://localhost:5000/api/pose/detect \
  -H "Content-Type: application/json" \
  -d '{"image":"base64_encoded_image_string","target_pose":"neck_stretch"}'
```

### Using Postman
1. Import API collection from `docs/YogaPose_API_Collection.json`
2. Set environment variable `base_url` to `http://localhost:5000`
3. Run requests

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'mediapipe'`
**Solution**: 
```bash
pip install mediapipe
```

**Issue**: `MySQL connection failed`
**Solution**:
- Check MySQL service is running: `sudo service mysql status`
- Verify credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`

**Issue**: `Port 5000 already in use`
**Solution**:
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
# Or use different port
flask run --port=5001
```

### Frontend Issues

**Issue**: `vite: not found`
**Solution**:
```bash
npm install
```

**Issue**: `Cannot connect to backend`
**Solution**:
- Ensure backend is running
- Check `VITE_API_URL` in `.env`
- Verify CORS settings in backend

**Issue**: Camera not working
**Solution**:
- Ensure camera permissions granted in browser
- Check camera is not used by another application
- Try refreshing page

### ML Model Issues

**Issue**: `Model file not found`
**Solution**:
```bash
cd backend
python app/ml/train_model.py
```

**Issue**: Low accuracy (<80%)
**Solution**:
- Check dataset quality
- Increase training samples
- Tune hyperparameters in `train_model.py`
- Verify landmark extraction is working

---

## Monitoring & Logging

### Backend Logs
```bash
# View Flask logs
tail -f backend/logs/app.log

# View error logs
tail -f backend/logs/error.log
```

### Frontend Console
- Open browser DevTools (F12)
- Check Console for errors
- Network tab for API call inspection

### Performance Monitoring
- Backend: Flask-MonitoringDashboard
- Frontend: React DevTools Profiler

---

## Backup & Maintenance

### Database Backup
```bash
mysqldump -u yoga_user -p yoga_pose_db > backup_$(date +%Y%m%d).sql
```

### Database Restore
```bash
mysql -u yoga_user -p yoga_pose_db < backup_20240115.sql
```

### Model Retraining
```bash
cd backend
python app/ml/train_model.py
```

---

## Security Checklist

- [ ] Change default JWT secret keys
- [ ] Use HTTPS in production
- [ ] Enable CORS only for trusted origins
- [ ] Set strong database passwords
- [ ] Regular security updates
- [ ] Input validation on all endpoints
- [ ] Rate limiting on API calls
- [ ] Secure cookie settings

---

## Support & Resources

### Documentation
- API Docs: http://localhost:5000/api/docs
- Frontend: See `FRONTEND_ARCHITECTURE.md`
- Backend: See `BACKEND_ARCHITECTURE.md`

### External Resources
- MediaPipe Pose: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/

---

## Quick Commands Reference

```bash
# Start all services
cd backend && source venv/bin/activate && python run.py &
cd app && npm run dev &

# Stop all services
pkill -f "python run.py"
pkill -f "npm run dev"

# Rebuild frontend
cd app && npm run build

# Retrain model
cd backend && python app/ml/train_model.py

# Database reset
flask db downgrade base
flask db upgrade
python seed_data.py
```
