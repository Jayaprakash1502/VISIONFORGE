import React, { useState } from 'react';
import { Camera } from '../types';
import { Camera as CameraIcon, Plus, Video } from 'lucide-react';
import { api } from '../services/api';

interface CamerasPageProps {
  cameras: Camera[];
  onRefreshCameras?: () => void;
}

export const CamerasPage: React.FC<CamerasPageProps> = ({ cameras, onRefreshCameras }) => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');
  const [sourceType, setSourceType] = useState<'LOCAL_VIDEO' | 'RTSP' | 'WEBCAM'>('LOCAL_VIDEO');
  const [sourceUrl, setSourceUrl] = useState('data/videos/demo.mp4');
  const [loading, setLoading] = useState(false);

  const handleSaveCamera = async () => {
    if (!name.trim()) return;
    setLoading(true);
    try {
      await api.createCamera({
        name,
        location: location || 'Surveillance Location',
        source_type: sourceType,
        source_url: sourceUrl || 'data/videos/demo.mp4',
        enabled: true,
      });
      setShowAddModal(false);
      setName('');
      setLocation('');
      if (onRefreshCameras) onRefreshCameras();
    } catch (e) {
      console.error('Failed to create camera:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <CameraIcon className="w-5 h-5 text-[#8B7FC7]" />
            <span>CAMERA MANAGEMENT MATRIX</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Configure surveillance streams, RTSP links, and polygon zone bindings</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 bg-[#8B7FC7] hover:bg-[#A99BE0] text-white px-4 py-2 rounded-lg text-xs font-semibold shadow-sm transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add New Camera</span>
        </button>
      </div>

      {/* Camera Grid Table */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cameras.map((cam) => (
          <div key={cam.id} className="bg-white border border-[#E2DFEC] rounded-xl p-5 space-y-4 shadow-sm">
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-[#F7F6FB] border border-[#E2DFEC] rounded-xl text-[#8B7FC7]">
                  <Video className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-[#242331]">{cam.name}</h3>
                  <p className="text-xs text-[#AAA6BA]">{cam.location || 'Unspecified location'}</p>
                </div>
              </div>
              <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded bg-[#5FBF9F]/10 text-[#5FBF9F] border border-[#5FBF9F]/30">
                {cam.status}
              </span>
            </div>

            <p className="text-xs text-[#242331]/80 leading-relaxed">{cam.description || 'No detailed description.'}</p>

            <div className="space-y-1.5 pt-3 border-t border-[#E2DFEC] text-xs font-mono">
              <div className="flex justify-between text-[#AAA6BA]">
                <span>Source Type:</span>
                <span className="text-[#242331] font-semibold">{cam.source_type}</span>
              </div>
              <div className="flex justify-between text-[#AAA6BA] truncate">
                <span>Source URL:</span>
                <span className="text-[#8B7FC7] font-semibold truncate max-w-[180px]">{cam.source_url}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Camera Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-[#242331]/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white border border-[#E2DFEC] rounded-xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-[#242331]">Add Camera Source</h3>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-[#AAA6BA] mb-1 font-semibold">Camera Name</label>
                <input
                  type="text"
                  placeholder="e.g. Camera 05 (South Gate Foyer)"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-[#F7F6FB] border border-[#E2DFEC] rounded px-3 py-2 text-[#242331]"
                />
              </div>
              <div>
                <label className="block text-[#AAA6BA] mb-1 font-semibold">Location</label>
                <input
                  type="text"
                  placeholder="e.g. Perimeter Gate 4"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full bg-[#F7F6FB] border border-[#E2DFEC] rounded px-3 py-2 text-[#242331]"
                />
              </div>
              <div>
                <label className="block text-[#AAA6BA] mb-1 font-semibold">Source Type</label>
                <select
                  value={sourceType}
                  onChange={(e) => setSourceType(e.target.value as any)}
                  className="w-full bg-[#F7F6FB] border border-[#E2DFEC] rounded px-3 py-2 text-[#242331]"
                >
                  <option value="LOCAL_VIDEO">LOCAL_VIDEO (.mp4)</option>
                  <option value="RTSP">RTSP Stream</option>
                  <option value="WEBCAM">Webcam Device</option>
                </select>
              </div>
              <div>
                <label className="block text-[#AAA6BA] mb-1 font-semibold">Source URL / File Path</label>
                <input
                  type="text"
                  placeholder="data/videos/demo.mp4 or rtsp://..."
                  value={sourceUrl}
                  onChange={(e) => setSourceUrl(e.target.value)}
                  className="w-full bg-[#F7F6FB] border border-[#E2DFEC] rounded px-3 py-2 text-[#242331]"
                />
              </div>
            </div>
            <div className="flex justify-end space-x-2 pt-2">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-1.5 bg-[#F7F6FB] border border-[#E2DFEC] text-[#242331] text-xs rounded font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveCamera}
                disabled={loading}
                className="px-4 py-1.5 bg-[#8B7FC7] text-white text-xs rounded font-semibold disabled:opacity-50"
              >
                {loading ? 'Saving...' : 'Save Camera'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
