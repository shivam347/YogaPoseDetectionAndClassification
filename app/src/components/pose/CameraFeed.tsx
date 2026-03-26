import { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';
import { Button } from '@/components/ui/button';
import { Camera, CameraOff, RefreshCw } from 'lucide-react';

interface CameraFeedProps {
  onFrame?: (imageSrc: string) => void;
  isProcessing?: boolean;
  mirrored?: boolean;
}

const CameraFeed = ({ onFrame, isProcessing = false, mirrored = true }: CameraFeedProps) => {
  const webcamRef = useRef<Webcam>(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');

  const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: facingMode,
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      stream.getTracks().forEach(track => track.stop());
      setHasPermission(true);
      setIsCameraOn(true);
    } catch (err) {
      setHasPermission(false);
      console.error('Camera permission denied:', err);
    }
  };

  const stopCamera = () => {
    setIsCameraOn(false);
    if (webcamRef.current) {
      const stream = webcamRef.current.video?.srcObject as MediaStream;
      stream?.getTracks().forEach(track => track.stop());
    }
  };

  const toggleCamera = () => {
    if (isCameraOn) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  const switchCamera = () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user');
  };

  // Capture frames for processing
  useEffect(() => {
    if (!isCameraOn || !onFrame) return;

    const interval = setInterval(() => {
      if (webcamRef.current && !isProcessing) {
        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
          onFrame(imageSrc);
        }
      }
    }, 200); // 5 FPS

    return () => clearInterval(interval);
  }, [isCameraOn, onFrame, isProcessing]);

  if (hasPermission === false) {
    return (
      <div className="relative w-full aspect-video bg-gray-100 rounded-2xl flex flex-col items-center justify-center p-8">
        <CameraOff className="w-16 h-16 text-gray-400 mb-4" />
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Camera Access Denied</h3>
        <p className="text-sm text-gray-500 text-center mb-4">
          Please allow camera access in your browser settings to use pose detection.
        </p>
        <Button onClick={startCamera} variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Camera Container */}
      <div className="relative w-full aspect-video bg-gray-900 rounded-2xl overflow-hidden shadow-2xl">
        {isCameraOn ? (
          <>
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              mirrored={mirrored}
              className="w-full h-full object-cover"
            />
            
            {/* Recording Indicator */}
            <div className="absolute top-4 left-4 flex items-center gap-2 bg-black/50 backdrop-blur-sm rounded-full px-3 py-1">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span className="text-xs text-white font-medium">LIVE</span>
            </div>

            {/* Processing Indicator */}
            {isProcessing && (
              <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm rounded-full px-3 py-1">
                <span className="text-xs text-white font-medium">Processing...</span>
              </div>
            )}
          </>
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
            <div className="w-20 h-20 rounded-full bg-white/10 flex items-center justify-center mb-4">
              <Camera className="w-10 h-10 text-white/50" />
            </div>
            <p className="text-white/70 text-sm">Camera is off</p>
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-3">
        <Button
          onClick={toggleCamera}
          className={`rounded-full px-6 ${
            isCameraOn 
              ? 'bg-red-500 hover:bg-red-600' 
              : 'bg-sage-500 hover:bg-sage-600'
          }`}
        >
          {isCameraOn ? (
            <>
              <CameraOff className="w-4 h-4 mr-2" />
              Stop
            </>
          ) : (
            <>
              <Camera className="w-4 h-4 mr-2" />
              Start Camera
            </>
          )}
        </Button>
        
        {isCameraOn && (
          <Button
            onClick={switchCamera}
            variant="secondary"
            className="rounded-full"
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
        )}
      </div>
    </div>
  );
};

export default CameraFeed;
