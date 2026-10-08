import React from 'react';
import { SecurityEvent } from '../types';
import { X, ShieldAlert, Camera, Clock, MapPin, Tag } from 'lucide-react';

interface EventDetailModalProps {
  event: SecurityEvent | null;
  onClose: () => void;
}

export const EventDetailModal: React.FC<EventDetailModalProps> = ({ event, onClose }) => {
  if (!event) return null;

  return (
    <div className="fixed inset-0 z-50 bg-[#242331]/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-[#E2DFEC] rounded-xl max-w-xl w-full p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-[#AAA6BA] hover:text-[#242331] p-1 rounded-lg hover:bg-[#F7F6FB] transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2.5 bg-[#D87586]/10 border border-[#D87586]/20 rounded-xl text-[#D87586]">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#242331]">{event.event_type}</h3>
            <p className="text-xs text-[#AAA6BA] font-mono">Event ID: {event.id}</p>
          </div>
        </div>

        <div className="space-y-4 my-5">
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC] flex items-center space-x-2">
              <Clock className="w-4 h-4 text-[#8B7FC7] flex-shrink-0" />
              <div>
                <span className="text-[#AAA6BA] block text-[10px] uppercase font-bold">Timestamp</span>
                <span className="font-semibold text-[#242331]">{new Date(event.timestamp).toLocaleString()}</span>
              </div>
            </div>

            <div className="p-3 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC] flex items-center space-x-2">
              <MapPin className="w-4 h-4 text-[#8B7FC7] flex-shrink-0" />
              <div>
                <span className="text-[#AAA6BA] block text-[10px] uppercase font-bold">Location</span>
                <span className="font-semibold text-[#242331]">{event.location || 'Main Entrance Lobby'}</span>
              </div>
            </div>

            <div className="p-3 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC] flex items-center space-x-2">
              <Tag className="w-4 h-4 text-[#D87586] flex-shrink-0" />
              <div>
                <span className="text-[#AAA6BA] block text-[10px] uppercase font-bold">Severity</span>
                <span className="font-extrabold text-[#D87586]">{event.severity}</span>
              </div>
            </div>

            <div className="p-3 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC] flex items-center space-x-2">
              <Camera className="w-4 h-4 text-[#5FBF9F] flex-shrink-0" />
              <div>
                <span className="text-[#AAA6BA] block text-[10px] uppercase font-bold">Status</span>
                <span className="font-bold text-[#5FBF9F]">{event.status}</span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC]">
            <h4 className="text-xs font-bold text-[#242331] mb-1">Description</h4>
            <p className="text-xs text-[#242331]/80 leading-relaxed">{event.description || 'No detailed description available.'}</p>
          </div>

          {event.detection_data && (
            <div className="p-4 bg-[#F7F6FB] rounded-xl border border-[#E2DFEC]">
              <h4 className="text-xs font-bold text-[#242331] mb-2">Detection Metadata</h4>
              <pre className="text-[11px] font-mono text-[#8B7FC7] bg-white p-3 rounded-lg border border-[#E2DFEC] overflow-x-auto">
                {JSON.stringify(event.detection_data, null, 2)}
              </pre>
            </div>
          )}
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-[#8B7FC7] hover:bg-[#A99BE0] text-white text-xs font-semibold rounded-lg shadow-sm transition"
          >
            Close Details
          </button>
        </div>
      </div>
    </div>
  );
};
