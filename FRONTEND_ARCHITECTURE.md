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