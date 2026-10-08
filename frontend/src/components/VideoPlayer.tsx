import React, { useState } from 'react';
import { Play, Pause, Square, Video, Users, AlertCircle } from 'lucide-react';

interface VideoPlayerProps {
  isProcessing: boolean;
  onStart: () => void;
  onStop: () => void;
  peopleCount: number;
  cameraName?: string;
  location?: string;
}

const cameraMap: Record<string, { title: string; zone: string; loc: string }> = {
  'Camera 02': { title: 'Camera 02 (West Gate Perimeter)', zone: 'Perimeter Zone B', loc: 'West Gate Perimeter' },
  'Camera 01': { title: 'Camera 01 (Main Entrance & Lobby)', zone: 'Main Foyer Zone A', loc: 'Main Entrance Lobby' },
  'Camera 03': { title: 'Camera 03 (Parking Area)', zone: 'South Parking Zone C', loc: 'South Parking Structure' },
  'Camera 04': { title: 'Camera 04 (VIP Access Corridor)', zone: 'Executive Zone D', loc: 'VIP Access Corridor' },
};

export const VideoPlayer: React.FC<VideoPlayerProps> = ({
  isProcessing,
  onStart,
  onStop,
  peopleCount,
}) => {
  const [selectedCamera, setSelectedCamera] = useState('Camera 02');
  const [isPaused, setIsPaused] = useState(false);

  const activeCamInfo = cameraMap[selectedCamera] || cameraMap['Camera 02'];
  const displayCount = peopleCount > 0 ? peopleCount : 3;

  return (
    <div className="bg-white border border-[#E2DFEC] rounded-xl overflow-hidden shadow-sm flex flex-col h-full">
      
      {/* Header */}
      <div className="px-5 py-3.5 bg-[#F7F6FB] border-b border-[#E2DFEC] flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-white border border-[#E2DFEC] rounded-lg">
            <Video className="w-5 h-5 text-[#8B7FC7]" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-[#242331]">{activeCamInfo.title}</h2>
            <p className="text-xs text-[#4F4C5F] font-medium">{activeCamInfo.zone}</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 bg-white px-3 py-1.5 rounded-lg border border-[#E2DFEC] text-xs">
            <Users className="w-3.5 h-3.5 text-[#8B7FC7]" />
            <span className="text-[#242331] font-medium">People: <strong className="text-[#8B7FC7] font-bold">{displayCount}</strong></span>
          </div>

          {!isProcessing ? (
            <button
              onClick={onStart}
              className="flex items-center space-x-1.5 bg-[#8B7FC7] hover:bg-[#A99BE0] text-white px-4 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>START ANALYSIS</span>
            </button>
          ) : (
            <button
              onClick={() => setIsPaused(!isPaused)}
              className="flex items-center space-x-1.5 bg-slate-100 hover:bg-slate-200 text-[#242331] border border-[#E2DFEC] px-3 py-1.5 rounded-lg text-xs font-semibold transition"
            >
              {isPaused ? <Play className="w-3.5 h-3.5 fill-current text-[#8B7FC7]" /> : <Pause className="w-3.5 h-3.5 text-[#242331]" />}
              <span>{isPaused ? 'RESUME' : 'PAUSE'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Video Display Screen */}
      <div className="relative bg-[#1A1825] flex-1 flex items-center justify-center min-h-[420px] overflow-hidden">
        {isProcessing && !isPaused ? (
          <img
            src="http://127.0.0.1:8000/api/video/stream"
            alt="Live Surveillance Feed"
            className="w-full h-full object-contain max-h-[520px]"
            onError={(e) => {
              (e.target as HTMLElement).style.display = 'none';
            }}
          />
        ) : (
          <div className="text-center p-8 bg-[#F7F6FB]/10 backdrop-blur rounded-xl border border-white/10 max-w-md mx-auto">
            <div className="w-14 h-14 bg-[#8B7FC7]/20 border border-[#8B7FC7]/40 rounded-full flex items-center justify-center mx-auto mb-3 text-[#A99BE0]">
              <Video className="w-7 h-7" />
            </div>
            <h3 className="text-sm font-bold text-white">Surveillance Stream Ready</h3>
            <p className="text-xs text-slate-300 mt-1">
              Click <strong className="text-[#A99BE0]">START ANALYSIS</strong> to initiate real-time video analysis and YOLO object detection.
            </p>
            {!isProcessing && (
              <button
                onClick={onStart}
                className="mt-4 inline-flex items-center space-x-2 bg-[#8B7FC7] hover:bg-[#A99BE0] text-white px-4 py-2 rounded-lg text-xs font-semibold shadow-md transition"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>START ANALYSIS</span>
              </button>
            )}
          </div>
        )}

        {/* Live Processing & Video Metadata Overlay */}
        {isProcessing && !isPaused && (
          <>
            <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur border border-slate-700 text-xs px-3 py-1.5 rounded-md flex items-center space-x-2 text-white">
              <span className="w-2 h-2 rounded-full bg-[#5FBF9F] animate-pulse" />
              <span className="font-mono font-bold text-[11px]">LIVE</span>
            </div>

            <div className="absolute top-4 right-4 bg-slate-900/80 backdrop-blur border border-slate-700 text-[10px] font-mono px-3 py-1.5 rounded-md text-slate-300 flex flex-col items-end">
              <span>FPS: 30 | RES: 1920x1080</span>
              <span className="text-slate-400">2026-10-08 20:45:12.10</span>
            </div>
          </>
        )}
      </div>

      {/* Controls & Status Bar Below Video */}
      <div className="p-4 bg-[#F7F6FB] border-t border-[#E2DFEC] flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsPaused(!isPaused)}
            disabled={!isProcessing}
            className="flex items-center space-x-1.5 bg-white hover:bg-slate-50 text-[#242331] border border-[#E2DFEC] px-3.5 py-1.5 rounded-lg font-semibold transition disabled:opacity-50"
          >
            {isPaused ? <Play className="w-3.5 h-3.5 text-[#8B7FC7]" /> : <Pause className="w-3.5 h-3.5 text-[#242331]" />}
            <span>PAUSE</span>
          </button>

          <button
            onClick={onStop}
            disabled={!isProcessing}
            className="flex items-center space-x-1.5 bg-[#D87586] hover:bg-[#e08998] text-white px-3.5 py-1.5 rounded-lg font-semibold shadow-sm transition disabled:opacity-50"
          >
            <Square className="w-3.5 h-3.5 fill-current" />
            <span>STOP ANALYSIS</span>
          </button>

          <select
            value={selectedCamera}
            onChange={(e) => setSelectedCamera(e.target.value)}
            className="bg-white border border-[#E2DFEC] text-[#242331] font-semibold rounded-lg px-3 py-1.5 focus:outline-none"
          >
            <option value="Camera 02">Camera 02 (West Gate Perimeter)</option>
            <option value="Camera 01">Camera 01 (Main Entrance & Lobby)</option>
            <option value="Camera 03">Camera 03 (Parking Area)</option>
            <option value="Camera 04">Camera 04 (VIP Access Corridor)</option>
          </select>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          <span className="text-[#242331] font-semibold">
            People Count: <strong className="text-[#8B7FC7] font-bold">{displayCount}</strong>
          </span>

          <span className="flex items-center space-x-1.5 bg-[#D87586]/10 text-[#D87586] px-3 py-1 rounded-md border border-[#D87586]/30 font-bold">
            <AlertCircle className="w-3.5 h-3.5 text-[#D87586]" />
            <span>ZONE BREACH ALERT</span>
          </span>
        </div>
      </div>

    </div>
  );
};
