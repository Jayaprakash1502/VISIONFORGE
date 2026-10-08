import React from 'react';
import { VideoPlayer } from '../components/VideoPlayer';
import { Camera, VideoStatus } from '../types';
import { Camera as CameraIcon, Radio, Users } from 'lucide-react';

interface LiveMonitoringPageProps {
  cameras: Camera[];
  videoStatus: VideoStatus;
  onStartVideo: () => void;
  onStopVideo: () => void;
}

export const LiveMonitoringPage: React.FC<LiveMonitoringPageProps> = ({
  cameras,
  videoStatus,
  onStartVideo,
  onStopVideo,
}) => {
  const secondaryFeeds = [
    { name: 'Camera 01 — Main Entrance & Lobby', zone: 'Zone A', count: 5, state: 'ACTIVE', statusBg: 'bg-[#5FBF9F]/10 text-[#5FBF9F] border-[#5FBF9F]/30' },
    { name: 'Camera 03 — Parking Area', zone: 'Zone C', count: 1, state: 'STANDBY', statusBg: 'bg-[#F7F6FB] text-[#AAA6BA] border-[#E2DFEC]' },
    { name: 'Camera 04 — VIP Access Corridor', zone: 'Zone D', count: 4, state: 'ACTIVE', statusBg: 'bg-[#5FBF9F]/10 text-[#5FBF9F] border-[#5FBF9F]/30' },
  ];

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <Radio className="w-5 h-5 text-[#5FBF9F]" />
            <span>LIVE MONITORING COMMAND CENTER</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Multi-stream video analytics monitoring matrix</p>
        </div>
        <div className="flex items-center space-x-2 bg-[#F7F6FB] px-3 py-1.5 rounded-lg border border-[#E2DFEC] text-xs">
          <span className="w-2 h-2 rounded-full bg-[#5FBF9F]" />
          <span className="font-semibold text-[#242331]">4 OPERATIONAL CAMERAS (3 ACTIVE STREAMS)</span>
        </div>
      </div>

      {/* Main Grid View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Primary Stream */}
        <div className="lg:col-span-2 min-h-[480px]">
          <VideoPlayer
            isProcessing={videoStatus.is_processing}
            onStart={onStartVideo}
            onStop={onStopVideo}
            peopleCount={videoStatus.current_people_count}
            cameraName={videoStatus.camera_name || 'Camera 02 (West Gate Perimeter)'}
            location={videoStatus.location || 'West Gate Perimeter'}
          />
        </div>

        {/* Secondary Stream Matrix */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold text-[#AAA6BA] uppercase tracking-wider">Secondary Camera Feeds</h3>

          {secondaryFeeds.map((feed, idx) => (
            <div key={idx} className="p-4 bg-white border border-[#E2DFEC] rounded-xl space-y-3 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <CameraIcon className="w-4 h-4 text-[#8B7FC7]" />
                  <span className="text-xs font-bold text-[#242331]">{feed.name}</span>
                </div>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${feed.statusBg}`}>
                  {feed.state}
                </span>
              </div>
              <div className="h-28 bg-[#F7F6FB] rounded-lg border border-[#E2DFEC] p-3 flex flex-col justify-between text-xs">
                <div className="flex justify-between text-[#AAA6BA]">
                  <span>Zone Binding: <strong className="text-[#242331]">{feed.zone}</strong></span>
                  <span className="flex items-center space-x-1 font-semibold text-[#8B7FC7]">
                    <Users className="w-3.5 h-3.5" />
                    <span>{feed.count} People</span>
                  </span>
                </div>
                <div className="flex items-center justify-between pt-2 border-t border-[#E2DFEC]/60 text-[11px] font-mono text-[#AAA6BA]">
                  <span>Mode: DEMO STREAM</span>
                  <span className="text-[#5FBF9F]">FPS: 30</span>
                </div>
              </div>
            </div>
          ))}

        </div>

      </div>

    </div>
  );
};
