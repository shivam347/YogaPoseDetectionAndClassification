# Yoga Pose Detection - Frontend Architecture

## Overview
React-based frontend for Yoga Pose Detection application with professional yoga-themed UI, real-time camera integration, and pose detection visualization.

## Tech Stack
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3.4+
- **UI Components**: shadcn/ui
- **Animation**: GSAP + ScrollTrigger
- **Camera**: react-webcam
- **HTTP Client**: Axios
- **State Management**: React Context API

## Project Structure
```
app/
├── src/
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── auth/               # Authentication components
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── layout/             # Layout components
│   │   │   ├── Navbar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── pose/               # Pose detection components
│   │   │   ├── CameraFeed.tsx
│   │   │   ├── PoseCanvas.tsx
│   │   │   ├── AccuracyMeter.tsx
│   │   │   └── PoseGuide.tsx
│   │   ├── exercise/           # Exercise components
│   │   │   ├── PainSelector.tsx
│   │   │   ├── AsanaCard.tsx
│   │   │   └── AsanaDetail.tsx
│   │   └── common/             # Shared components
│   │       ├── Hero.tsx
│   │       ├── FeatureCard.tsx
│   │       └── Testimonial.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── PainSelection.tsx
│   │   ├── AsanaList.tsx
│   │   ├── AsanaPractice.tsx
│   │   └── Profile.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useCamera.ts
│   │   ├── usePoseDetection.ts
│   │   └── useScrollAnimation.ts
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   └── PoseContext.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   └── poseService.ts
│   ├── types/
│   │   ├── auth.ts
│   │   ├── pose.ts
│   │   └── exercise.ts
│   ├── utils/
│   │   ├── landmarks.ts
│   │   ├── drawing.ts
│   │   └── helpers.ts
│   ├── styles/
│   │   └── globals.css
│   ├── App.tsx
│   └── main.tsx
├── public/
│   └── images/
├── index.html
├── tailwind.config.js
├── vite.config.ts
└── package.json
```

## Component Details

### Authentication Components

#### LoginForm.tsx
- Email/password input fields
- Form validation with error messages
- Loading state during submission
- Link to registration page

#### RegisterForm.tsx
- Name, email, password fields
- Password confirmation
- Form validation
- Success redirect to login

### Layout Components

#### Navbar.tsx
- Logo with yoga-themed icon
- Navigation links (Home, Poses, About, Contact)
- User menu when authenticated
- Glassmorphism effect on scroll

#### ProtectedRoute.tsx
- Checks authentication status
- Redirects to login if not authenticated
- Preserves intended route for post-login redirect

### Pose Detection Components

#### CameraFeed.tsx
- Webcam integration using react-webcam
- Start/stop camera controls
- Mirror mode for user-friendly view
- Error handling for camera permissions

#### PoseCanvas.tsx
- Canvas overlay on camera feed
- Draws pose landmarks and connections
- Real-time visualization of detected poses

#### AccuracyMeter.tsx
- Circular progress indicator
- Shows pose accuracy percentage
- Color-coded feedback (green/yellow/red)
- Animated transitions

#### PoseGuide.tsx
- Reference image of target pose
- Key alignment points
- Instructions for proper form

### Exercise Components

#### PainSelector.tsx
- Grid of pain type cards
- Options: Neck, Back, Shoulder, Knee, Stress, General
- Animated card hover effects
- Selection state management

#### AsanaCard.tsx
- Asana image thumbnail
- Name in English and Sanskrit
- Brief benefit description
- Difficulty level indicator

#### AsanaDetail.tsx
- Full asana information
- Large image
- Detailed benefits list
- Step-by-step instructions
- Camera start button

## Page Details

### Home.tsx
- Hero section with animated headline
- Feature highlights
- How it works section
- Testimonials
- CTA section

### Login.tsx / Register.tsx
- Centered auth forms
- Yoga-themed background
- Smooth transitions between forms

### Dashboard.tsx
- User welcome section
- Recent practice history
- Recommended exercises
- Progress statistics

### PainSelection.tsx
- Pain type selector grid
- Animated entrance
- Smooth navigation to asana list

### AsanaList.tsx
- Filtered asanas based on pain type
- Grid layout with AsanaCards
- Search and filter options

### AsanaPractice.tsx
- Split view: Camera + Guide
- Real-time pose detection
- Accuracy feedback
- Timer for hold duration

## Custom Hooks

### useAuth.ts
```typescript
const useAuth = () => {
  const { user, login, logout, register } = useContext(AuthContext);
  return { user, isAuthenticated: !!user, login, logout, register };
};
```

### useCamera.ts
```typescript
const useCamera = () => {
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const startCamera = () => {...};
  const stopCamera = () => {...};
  return { isActive, error, startCamera, stopCamera, videoRef };
};
```

### usePoseDetection.ts
```typescript
const usePoseDetection = (videoRef: RefObject<HTMLVideoElement>) => {
  const [landmarks, setLandmarks] = useState<Landmark[]>([]);
  const [accuracy, setAccuracy] = useState(0);
  const [detectedPose, setDetectedPose] = useState<string>('');
  // MediaPipe integration
  return { landmarks, accuracy, detectedPose, isLoading };
};
```

## Styling Guidelines

### Color Palette
```css
:root {
  --primary-bg: #FFFFFF;
  --text-dark: #000000;
  --text-gray: #333333;
  --text-light: #666666;
  --accent-sage: #8B9A7C;
  --accent-terracotta: #D4A574;
  --accent-lavender: #9B8FBF;
  --success: #4CAF50;
  --error: #F44336;
  --border: #E0E0E0;
}
```

### Typography
- **Headings**: Playfair Display, serif
- **Body**: Poppins, sans-serif
- **Icons**: Material Icons

### Animation Timing
```css
:root {
  --ease-breath: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-flow: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --duration-fast: 300ms;
  --duration-medium: 600ms;
  --duration-slow: 1000ms;
}
```

## API Integration

### Auth Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Exercise Endpoints
- `GET /api/exercises` - List all exercises
- `GET /api/exercises?pain_type=neck` - Filter by pain type
- `GET /api/exercises/:id` - Get exercise details

### Practice Endpoints
- `POST /api/practice` - Save practice session
- `GET /api/practice/history` - Get practice history

## State Management

### AuthContext
```typescript
interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}
```

### PoseContext
```typescript
interface PoseState {
  currentPose: Pose | null;
  accuracy: number;
  landmarks: Landmark[];
  isDetecting: boolean;
}
```

## Performance Optimizations

1. **Lazy Loading**: Route-based code splitting
2. **Image Optimization**: WebP format with fallbacks
3. **Canvas Optimization**: requestAnimationFrame for drawing
4. **Memoization**: React.memo for expensive components
5. **Debounce**: Input handlers and scroll events

## Security Considerations

1. **JWT Storage**: HttpOnly cookies
2. **API Calls**: Axios interceptors for token refresh
3. **Input Sanitization**: Prevent XSS attacks
4. **Camera Permissions**: Explicit user consent
5. **HTTPS**: All API communications

## Responsive Breakpoints
```css
/* Mobile */
@media (max-width: 768px) { ... }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* Desktop */
@media (min-width: 1025px) { ... }
```
